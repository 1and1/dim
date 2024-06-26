# Create a user with network_admin rights and a regular user
# make sure the users exist
# as user user
$ ndcli login -u user -p p
# as user network
$ ndcli login -u network -p p

# as user admin
$ ndcli create user-group networkgroup
$ ndcli modify user-group networkgroup grant network_admin
$ ndcli modify user-group networkgroup add user network

# network_admin user
# as user network
$ ndcli create pool testpool -u network
$ ndcli create container 12.0.0.0/8 -u network
INFO - Creating container 12.0.0.0/8 in layer3domain default
$ ndcli modify pool testpool add subnet 12.0.0.0/24 -u network
INFO - Created subnet 12.0.0.0/24 in layer3domain default
WARNING - Creating zone 0.0.12.in-addr.arpa without profile
WARNING - Primary NS for this Domain is now localhost.
$ ndcli create user-group testgroup -u network
$ ndcli modify user-group testgroup add user user -u network
$ ndcli modify user-group testgroup grant allocate testpool -u network

# Regular user
# as user user
$ ndcli create pool testpool2 -u user
ERROR - Permission denied (can_network_admin)
$ ndcli list pool testpool -u user
INFO - Total free IPs: 254
prio subnet      gateway free total
   1 12.0.0.0/24          254   256
$ ndcli create user-group testgroup2 -u user
ERROR - Permission denied (can_create_groups)
$ ndcli modify user-group testgroup add user user -u user
ERROR - Permission denied (can_edit_group testgroup)
$ ndcli modify user-group testgroup remove user user -u user
ERROR - Permission denied (can_edit_group testgroup)
$ ndcli modify user-group testgroup grant allocate testpool -u user
ERROR - Permission denied (can_network_admin)

# Test deleting groups while they still have members
# as user network
$ ndcli create user-group testgroup2 -u network
$ ndcli modify user-group testgroup2 add user user -u network
$ ndcli list user user groups -u network
group
all_users
testgroup
testgroup2
$ ndcli delete user-group testgroup2 -u network
$ ndcli list user user groups -u network
group
all_users
testgroup

# network_admin users cannot grant network_admin rights
$ ndcli modify user-group testgroup grant network_admin -u network
ERROR - Permission denied (can_grant_access testgroup network_admin)
# network_admin users cannot change network_admin groups
$ ndcli modify user-group networkgroup add user user -u network
ERROR - Permission denied (can_edit_group networkgroup)
# network_admin users can rename and delete normal groups
$ ndcli rename user-group testgroup to testgroup1 -u network
$ ndcli delete user-group testgroup1 -u network
$ ndcli delete container 12.0.0.0/8 -u network
INFO - Deleting container 12.0.0.0/8 from layer3domain default
