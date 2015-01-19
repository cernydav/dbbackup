# dbbackup
Simple python mysql backup tool. Ready for scheduling by cron. This python script is used for mysql database backup
using mysqldump utility.

	Written by : David Cerny
	Website: http://senman.cz
	Created date: Jan 19, 2015
	Last modified: Jan 19, 2015
	Tested with : Python 2.7.6
	Thank you for inspiration: Rahul Kumar, David Goodwin, Blair Conrad, Martin Miller

Some scheduling CRON TIps in http://tecadmin.net/crontab-in-linux-with-20-examples-of-cron-schedule/

	to run this every day in 2am  
	0 2 * * * /usr/bin/python python.py


## Versions

There are two versions. 

* Simple
* Cofigurable

Simple uses one file with all configuration in it. Configurable is version splitted to two files one is config which should go to /etc/ and second is will be executable which will go to /usr/share/ and /usr/bin/

## Notice 

This script must be run with root privileges.




