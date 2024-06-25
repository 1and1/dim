mysql -u root pdns_int </docker-entrypoint-initdb.d/pdns.sql.txt
mysql -u root pdns_pub < /docker-entrypoint-initdb.d/pdns.sql.txt
