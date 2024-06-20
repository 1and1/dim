#!/bin/bash

# This script set empty password for user root to allow to connect to the database anonymously
# Tested on Rocky linux 9

sudo mysql -uroot -e "SET PASSWORD FOR 'root'@'localhost' = PASSWORD('');"
sudo mysql -uroot -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '';"
sudo mysql -uroot -e "FLUSH PRIVILEGES;"
sudo mysql -uroot -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '';"
sudo mysql -uroot -e "FLUSH PRIVILEGES;"
sudo mysql -uroot -e "SET PASSWORD FOR 'root'@'localhost' = PASSWORD('');"
