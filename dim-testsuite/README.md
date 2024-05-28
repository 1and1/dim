# dim-testsuite

This is the test suite to run tests over all the components of dim, including
ndcli, dimclient, dim itself, the output and some more.

**DO NOT USE THE TEST SUITE ON YOUR PRODUCTION DATA!**

As of now, make sure that your home *does not* contain a vaild `.ndclirc` and `.ndcli.cookie`.
If ndcli finds valid login information these might get use. In consequence the tests will be
run on the production DIM.

## requirements

You need a running mysql instance listening on 127.0.0.1:3307 with the following databases:

```sql
create database dim;
create database pdns1;
create database pdns2;
```

and the following users:

```sql
grant all on pdns1.* to 'pdns1'@'localhost' identified by 'pdns';
grant all on pdns2.* to 'pdns2'@'localhost' identified by 'pdns';
grant all on dim.* to 'dim'@'localhost' identified by 'dim';
```

You also need to grant the user running the tests full rights on the databases:

```sql
create user 'janedoe'@'localhost';
grant all on pdns1.* to 'janedoe'@'localhost';
grant all on pdns2.* to 'janedoe'@'localhost';
grant all on dim.* to 'janedoe'@'localhost';
```

If MariaDB does not startup please try to disable SELinux and try again.

The database files should be on a tmpfs to have a bit better performance for testing.

Then create the file `/etc/dim/dim.cfg` with a production like configuration.
It must contain the database credentials, so that the server can connect to the database.

Example config:

```ini
### Database
SQLALCHEMY_DATABASE_URI = 'mysql://dim:dim@127.0.0.1:3307/dim'
DB_LOCK_TIMEOUT = 120

# Set SECRET_KEY to a random string
# The security of this application is compromised if SECRET_KEY is leaked
SECRET_KEY = 'testkey'
PERMANENT_SESSION_LIFETIME = 30 * 24 * 3600 # 1 month
TEMPORARY_SESSION_LIFETIME = 24 * 3600            # 1 day


### Logging
import logging, logging.handlers, sys
LOGGING_LEVEL = logging.DEBUG
LOGGING_HANDLER = logging.StreamHandler(sys.stderr)
#LOGGING_HANDLER = logging.handlers.SysLogHandler(address='/dev/log', facility='local0')


### DNS
DNS_DEFAULT_REFRESH  = 14400  # 4 hours
DNS_DEFAULT_RETRY    = 3600   # 1 hour
DNS_DEFAULT_EXPIRE   = 605000 # 7 days
DNS_DEFAULT_MINIMUM  = 86400  # 1 day (Min. TTL)
DNS_DEFAULT_ZONE_TTL = 86400  # 1 day (Default. TTL)

# list of ipspaces which are allowed to exist multiple times in dim (layer3domains)
# in general only rfc1918 ip should be allowed
LAYER3DOMAIN_WHITELIST = ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', '100.64.0.0/10']


### Debugging
SQLALCHEMY_DATABASE_URI_TEST = 'mysql://dim:dim@127.0.0.1:3307/dim'
PDNS_DATABASE_URI_TEST = 'mysql://pdns1:pdns@127.0.0.1:3307/pdns1'
SYNC_PDNS_OUTPUT = False
DEBUG = False
SQLALCHEMY_LOG = False
```

The following programs need to be installed:

* python3-devel
* colordiff
* make
* mariadb-devel
* openldap-devel
* gcc

### ndcli test suite

To run the ndcli test suite, make sure the mysql database is up and running.

Then call `make`.
It will proceed and build a virtual environment and install the tools needed
into it, and initialize the databases.

After that it will start the dim server and start making ndcli calls against
the server.

To control the location of the virtual environment, the output directory, or
the log directory, use the variables `VDIR`, `ODIR` and `LDIR`.

```shell
make VDIR=/tmp/venv ODIR=/tmp/test_output LDIR=/tmp/test_logs
```

If you want to skip the database initialization or installing of dependencies,
let *make* run the tests directly by using `make test`.

To run only specific testfiles, use the variable `TESTS` for `make test` after
you've created the virtual environment.

```shell
make test TESTS="<test1> <test2>"
```

`runtest.py` will look in the `t` directory for the specific testcases and run
only the ones specified in `TESTS`. After the case was run, your dim environment will have
exactly the state it broke in, so you can poke into it with ndcli, for example:

```shell
$VDIR/bin/ndcli list pools
```

### pytest test suite

To run the pytest test suite, make sure the mysql database is up and running.

Then call `make install`, or `make install-dev` (editable setup, changes to the code tree
will affect the virtual environment after creation).
It will proceed and build a virtual environment and install the tools needed
into it.

If you did not initialize the databases yet, run `make db` to do so.

To run the pytests, call `make pytest`.

To run only specific pytests, use the variable `PYTESTS` for `make pytest` after
you've created the virtual environment.

```shell
make pytest PYTESTS="<test1> <test2>"
```

This will run only the pytest(s) you specified.
For this, you'll need to pass the test *class names*, not the filenames:
e.g. `make pytest PYTESTS="AllocatorTest"` to run the tests for that class,
which is from the `tests/allocator_test.py` file.
