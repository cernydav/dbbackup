#!/usr/bin/python
###########################################################
#
# This python script is used for mysql database backup
# using mysqldump utility.
#
# Written by : David Cerny
# Website: http://senman.cz
# Created date: Jan 19, 2015
# Last modified: Jan 19, 2015
# Tested with : Python 2.7.6
# Thank you for inspiration: Rahul Kumar, David Goodwin, Blair Conrad, Martin Miller
#
# Some scheduling CRON TIps in http://tecadmin.net/crontab-in-linux-with-20-examples-of-cron-schedule/
#
# to run this every day in 2am  
# 0 2 * * * /usr/bin/python python.py
#
##########################################################

#Importing the modules
import os
import ConfigParser
import time
import shutil


# IMPORTANT Application Settings
BACKUP_PATH = "/var/backups/mysql/"
BACKUP_LIFE_IN_DAYS = 7 # days



# ADDITIONAL Application Settings
DATETIME = time.strftime('%Y-%m-%d')



# On Debian, /etc/mysql/debian.cnf contains 'root' a like login and password.
config = ConfigParser.ConfigParser()
config.read("/etc/mysql/debian.cnf")
username = config.get('client', 'user')
password = config.get('client', 'password')
hostname = config.get('client', 'host')



def removeOldDirs(dirPathList):
    """
    return true
    """
    for dirPath in dirPathList:
        #print dirPath
        shutil.rmtree(dirPath)


def getOldDirs(dirPath, olderThanDays):
    """
    return a list of all subfolders under dirPath older than olderThanDays
    """
    olderThanDays *= 86400 # convert days to seconds
    present = time.time()
    directories = []
    for root, dirs, files in os.walk(dirPath, topdown=False):
        for name in dirs:
            subDirPath = os.path.join(root, name)
            if (present - os.path.getmtime(subDirPath)) > olderThanDays:
                directories.append(subDirPath)  
    return directories


TODAYBACKUPPATH = BACKUP_PATH + DATETIME
removeOldDirs (getOldDirs(BACKUP_PATH, BACKUP_LIFE_IN_DAYS))


# Checking if backup folder already exists or not. If not exists will create it.
#print "creating backup folder"
if not os.path.exists(TODAYBACKUPPATH):
    os.makedirs(TODAYBACKUPPATH)


# Get a list of databases with :
database_list_command="mysql -u %s -p%s -h %s --silent -N -e 'show databases'" % (username, password, hostname)
for database in os.popen(database_list_command).readlines():
    database = database.strip()
    if database == 'information_schema':
        continue
    if database == 'performance_schema':
        continue

    filestamp = time.strftime('%H-%M-%S')
    filename =  TODAYBACKUPPATH +"/" + "%s-%s.sql" % (filestamp, database)
    os.popen("mysqldump --single-transaction -u %s -p%s -h %s -d %s | gzip -c > %s.gz" % (username, password, hostname, database, filename))



