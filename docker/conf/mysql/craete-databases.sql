create database `pdns_int`;
create database `pdns_pub`;
create database `dim`;

CREATE USER 'dim_user'@'10.10.0.%' IDENTIFIED BY 'dim_pass';
CREATE USER 'dim_pdns_int_user'@'10.10.0.%' IDENTIFIED BY 'SuperSecret1';
CREATE USER 'dim_pdns_pub_user'@'10.10.0.%' IDENTIFIED BY 'SuperSecret2';
CREATE USER 'pdns_pub_user'@'10.10.0.%' IDENTIFIED BY 'SuperSecret3';
CREATE USER 'pdns_int_user'@'10.10.0.%' IDENTIFIED BY 'SuperSecret4';

GRANT ALL ON dim.* TO 'dim_user'@'10.10.0.%';
GRANT INSERT,UPDATE,DELETE,SELECT ON pdns_int.* TO 'dim_pdns_int_user'@'10.10.0.%';
GRANT INSERT,UPDATE,DELETE,SELECT ON pdns_pub.* TO 'dim_pdns_pub_user'@'10.10.0.%';
GRANT SELECT ON pdns_pub.* TO 'pdns_pub_user'@'10.10.0.%';
GRANT SELECT ON pdns_int.* TO 'pdns_int_user'@'10.10.0.%';
