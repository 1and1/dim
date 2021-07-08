

import logging
import sys

import ldap
from flask import current_app as app

from dim import db
from dim.models import Group, User, GroupMembership, Department
from dim.transaction import time_function, transaction


class LDAP(object):
    def __init__(self):
        ldap_server = app.config['LDAP_SERVER']
        try:
            self.conn = ldap.initialize(ldap_server, bytes_mode=False)
            self.conn.set_option(ldap.OPT_TIMEOUT, app.config['LDAP_OPT_TIMEOUT'])
            self.conn.set_option(ldap.OPT_TIMELIMIT, app.config['LDAP_OPT_TIMELIMIT'])
            self.conn.set_option(ldap.OPT_NETWORK_TIMEOUT, app.config['LDAP_OPT_NETWORK_TIMEOUT'])
            self.conn.simple_bind_s()
        except:
            logging.exception('Error connecting to ldap server %s', ldap_server)
            raise

    def query(self, base, filter):
        try:
            if filter:
                return self.conn.search_s(base, filterstr=filter, scope=ldap.SCOPE_ONELEVEL)
            else:
                return self.conn.search_s(base, scope=ldap.SCOPE_ONELEVEL)
        except:
            logging.exception('Error in LDAP query %s %s', base, filter)
            raise

    def users(self, filter):
        '''Return the set of usernames matching the ldap query.'''
        def fix_int(s): return int(s) if s is not None else s
        return [User(username=u[1]['o'][0].decode('utf-8'),
                     ldap_cn=u[1]['cn'][0].decode('utf-8'),
                     ldap_uid=fix_int(u[1]['uid'][0]),
                     department_number=fix_int(u[1]['departmentNumber'][0]),
                     register=False)
                for u in self.query(app.config['LDAP_USER_BASE'], filter)]

    def departments(self, filter):
        '''Return the list of departments'''
        res = self.query(app.config['LDAP_DEPARTMENT_BASE'], filter)
        if not res:
            return []
        else:
            return [Department(department_number=int(dept[1]['ou'][0]),
                               name=dept[1]['cn'][0].decode('utf-8'))
                    for dept in res]


def sync_departments(ldap):
    '''Update the department table'''
    db_departments = Department.query.all()
    ldap_departments = dict((dep.department_number, dep) for dep in ldap.departments(None))
    # handle renamed or deleted departments
    for ddep in db_departments:
        ldep = ldap_departments.get(ddep.department_number)
        if ldep:
            if ddep.name != ldep.name:
                logging.info('Renaming department %s to %s' % (ddep.name, ldep.name))
                ddep.name = ldep.name
            del ldap_departments[ddep.department_number]
        else:
            logging.info('Deleting department %s' % ddep.name)
            db.session.delete(ddep)
    # handle new departments
    for ldep in list(ldap_departments.values()):
        logging.info('Creating department %s' % ldep.name)
        db.session.add(ldep)


def log_stdout(message):
    logging.info(message)
    print(message)


def sync_users(ldap):
    '''Update the user table ldap_cn, ldap_uid and department_number fields'''
    db_users = User.query.all()
    ldap_users = dict((u.username, u)
                      for u in ldap.users('(|%s)' % ''.join('(o=%s)' % u.username for u in db_users)))
    for db_user in db_users:
        ldap_user = ldap_users.get(db_user.username)
        if ldap_user:
            if db_user.ldap_cn != ldap_user.ldap_cn:
                logging.info('User %s changed cn from %s to %s' %
                             (db_user.username,
                              db_user.ldap_cn,
                              ldap_user.ldap_cn))
                db_user.ldap_cn = ldap_user.ldap_cn
            if db_user.department_number != ldap_user.department_number:
                logging.info('User %s moved from department_number %s to %s' %
                             (db_user.username,
                              db_user.department_number,
                              ldap_user.department_number))
                db_user.department_number = ldap_user.department_number
            if db_user.ldap_uid != ldap_user.ldap_uid:
                logging.info('User %s changed uid from %s to %s' %
                             (db_user.username,
                              db_user.ldap_uid,
                              ldap_user.ldap_uid))
                db_user.ldap_uid = ldap_user.ldap_uid
        elif db_user.ldap_uid:
            log_stdout('Deleting user %s' % db_user.username)
            db.session.delete(db_user)


@time_function
@transaction
def ldap_sync():
    '''Update Users, Group, and Departments from LDAP'''
    ldap = LDAP()

    if sys.stdout.isatty():
        logging.getLogger().addHandler(logging.StreamHandler(sys.stderr))

    sync_departments(ldap)
    sync_users(ldap)

    # Synchronize group members
    ldap_users = {}  # map department_number to list of usernames
    for group in Group.query.filter(Group.department_number != None).all():  # noqa
        search_results = ldap.departments('ou=%s' % group.department_number)
        if len(search_results) == 0:
            group.department_number = None
            log_stdout('Department %s %s was deleted and had the following members from LDAP: %s' % (
                group.department_number,
                group.name,
                ' '.join(gm.user.username for gm in GroupMembership.query
                         .filter(GroupMembership.from_ldap)
                         .filter(GroupMembership.group == group).all())))
        else:
            dept = search_results[0]
            if dept.name != group.name:
                new_name = dept.name
                if Group.query.filter(Group.name == new_name).count():
                    # DIM-209 append id to department name to generate an unique user group name
                    new_name += '_%s' % dept.department_number
                logging.info('Renaming group %s to %s' % (group.name, new_name))
                group.name = new_name
            ldap_users[group.department_number] = \
                [u.username for u in ldap.users('departmentNumber=%s' % dept.department_number)]
    # Remove all users added by a ldap query that are no longer present in the group
    for membership in GroupMembership.query.filter(GroupMembership.from_ldap).all():  # noqa
        if membership.group.department_number is None or \
           membership.user.username not in ldap_users[membership.group.department_number]:
            logging.info('User %s was removed from group %s' %
                         (membership.user.username, membership.group.name))
            membership.group.remove_user(membership.user)
    # Add new users to groups
    for group in Group.query.filter(Group.department_number != None).all():  # noqa
        group_users = set([u.username for u in group.users])
        for username in [u for u in ldap_users[group.department_number] if u not in group_users]:
            user = User.query.filter_by(username=username).first()
            if user is None:
                ldap_search = ldap.users('o=%s' % username)
                if ldap_search:
                    lu = ldap_search[0]
                    user = User(username=username,
                                ldap_uid=lu.ldap_uid,
                                ldap_cn=lu.ldap_cn,
                                department_number=lu.department_number)
                    db.session.add(user)
                    db.session.add(GroupMembership(user=user, group=group, from_ldap=True))
                    group_users.add(username)
                    logging.info('User %s was created and added to group %s', username, group.name)
            else:
                logging.info('User %s was added to group %s', username, group.name)
                db.session.add(GroupMembership(user=user, group=group, from_ldap=True))
                group_users.add(username)
