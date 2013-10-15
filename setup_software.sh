#!/bin/bash -x

git pull

apt-get update
apt-get dist-upgrade
apt-get install -y git python-pip git-review libxml2-dev libxml2-utils libxslt-dev libmysqlclient-dev pep8 postgresql-server-dev-9.1 python2.7-dev python-coverage python-netaddr python-mysqldb mysql-server python-git virtualenvwrapper python-numpy

cp etc/my.cnf /etc/mysql/
cp etc/usr.sbin.mysqld /etc/apparmor.d/
cp etc/mysql-server /etc/logrotate.d/
cp etc/logrotate /etc/cron.daily/

mkdir -p /var/log/mysql
touch /var/log/mysql/slow-queries.log
chown mysql.mysql /var/log/mysql/slow-queries.log

chmod ugo+rx /var/log/mysql
chmod ugo+r /var/log/syslog /var/log/mysql/slow-queries.log /var/log/mysql/error.log

chown -R mysql.mysql /srv/mysql

/usr/sbin/logrotate /etc/logrotate.conf

/etc/init.d/apparmor restart
/etc/init.d/mysql restart

# Cleanup git checkouts
for dir in `find /srv/git-checkouts/openstack/ -maxdepth 1 -mtime +14 | grep nova_refs`
do
  echo "Cleanup $dir"
  rm -rf $dir
done
