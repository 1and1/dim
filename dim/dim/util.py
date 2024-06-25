import logging
import re
import subprocess
import time
from contextlib import contextmanager

from flask_sqlalchemy import get_debug_queries
from sqlalchemy.orm import class_mapper, defer


_MAX_LENGTH = 300


def safe_repr(obj, short=True):
    try:
        result = repr(obj)
    except Exception:
        result = object.__repr__(obj)
    if not short or len(result) < _MAX_LENGTH:
        return result
    return result[:_MAX_LENGTH] + ' [truncated]...'


@contextmanager
def timing(label):
    start = time.time()
    yield
    print(('Time for %s: %.3f' % (label, time.time() - start)))


def defer_except(entity, cols, path=()):
    m = class_mapper(entity)
    defer_columns = set(p.key for p
                        in m.iterate_properties
                        if hasattr(p, 'columns')).difference(cols)
    return [defer(*(list(path) + [k])) for k in defer_columns]


@contextmanager
def print_queries():
    start_len = len(get_debug_queries())
    try:
        yield
    finally:
        for q in get_debug_queries()[start_len:]:
            try:
                print((">>> %.3f" % q.duration, q.statement % tuple(repr(p) for p in q.parameters)))
            except:
                print((q.statement, q.parameters))
            print()
        print((len(get_debug_queries()) - start_len, "queries"))


def printquery(statement, bind=None):
    """
    print a query, with values filled in
    for debugging purposes *only*
    for security, you should always separate queries from their values
    please also note that this function is quite slow
    """
    import sqlalchemy.orm
    if isinstance(statement, sqlalchemy.orm.Query):
        if bind is None:
            bind = statement.session.get_bind(statement._mapper_zero_or_none())
        statement = statement.statement
    elif bind is None:
        bind = statement.bind

    dialect = bind.dialect
    compiler = statement._compiler(dialect)

    class LiteralCompiler(compiler.__class__):
        def visit_bindparam(
                self, bindparam, within_columns_clause=False,
                literal_binds=False, **kwargs):
            return super(LiteralCompiler, self).render_literal_bindparam(
                bindparam,
                within_columns_clause=within_columns_clause,
                literal_binds=literal_binds, **kwargs)

    compiler = LiteralCompiler(dialect, statement)
    print((compiler.process(statement)))


def make_fqdn(target, zone_name):
    if target.endswith('.'):
        return target
    elif target == '@':
        return zone_name + '.'
    else:
        if zone_name != '':
            return target + '.' + zone_name + '.'
        return target + '.'


def email2fqdn(string):
    name, host = string.split('@')
    return '%s.%s.' % (name.replace('.', '\\.'), host)


def fqdn2email(string):
    name, host = re.split(r'(?<!\\)\.', string, 1)
    return '%s@%s' % (name.replace('\\.', '.'), host[:-1])


def strip_dot(fqdn):
    if fqdn.endswith('.'):
        return fqdn[:-1]


def is_reverse_zone(zone):
    return zone.endswith('in-addr.arpa') or zone.endswith('ip6.arpa')


def run(command):
    logging.info('Running ' + ' '.join(command))
    p = subprocess.Popen(command,
                         close_fds=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return p.returncode, stdout, stderr
