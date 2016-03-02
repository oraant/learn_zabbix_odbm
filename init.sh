#!/bin/bash

#basepath=/usr/lib/zabbix/externalscripts/zabbix-odbm
basepath=/root/zabbix-odbm
cp $basepath/lib/zabbix-odbm /etc/init.d/ && chkconfig --add zabbix-odbm
