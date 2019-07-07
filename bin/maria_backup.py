#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Project description
 __author__ = "chenqh"
 __date__: "2016/4/29"
 __company__: inno-view.cn
 __version__: "0.1"
 __note__: 脚本依赖percona-xtrabackup 2.3，请在使用前安装xtrabackup工具。
"""

import os
from backup_config import BackupConfig
from cmd_execute import CommandExecuter
from file_action import FileAction
from logerer import Logerer
from timer import Timer
        
class MariaBackup(object):
    apphome = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
    def __init__(self):
        bc = BackupConfig(MariaBackup.apphome + "/etc/config")
        self.dbhost = bc.getHost()
        self.dbport = bc.getPort()
        self.dbuser = bc.getUser()
        self.dbpasswd = bc.getPasswd()
        self.dbmycnf = bc.getMycnf()
        self.dbsock = bc.getSocket()

        self.bakdir = bc.getBakdir()
        self.bakkeep = bc.getBakkeep()

    def putConf(self):
        logger = Logerer("MariaBackup", apphome + "/log/config.log").getLoger()
        logger.info("host:" + self.dbhost)
        logger.info("port:" + self.dbport)
        logger.info("user:" + self.dbuser)
        logger.info("passwd:" + self.dbpasswd)
        logger.info("mycnf:" + self.dbmycnf)
        logger.info("bakdatadir:" + self.bakdir)
        logger.info("keepcycles:" + self.bakkeep)

    """ 本周是否已经全备 """
    def existFullbackup(self, backupdir):
        fa = FileAction()
        fdir = fa.getFulldir(backupdir)
        if fdir:
            return True
        else:
            return False

    """ 本周内昨天的增备是否存在 """
    def existIncrebackup(self, backupdir):
        fa = FileAction()
        fdir = fa.getIncredir(backupdir)
        if fdir:
            return True
        else:
            return False

    def backupFull(self):
        # 目录名组成：备份目录 + 周数 + full + 当前时间
        backdatadir = self.bakdir + Timer.getWeeks() + "_full_" + Timer.getDate()
        # print backdatadir
        backupcmd = CommandExecuter(xtra="/bin/xtrabackup",cnf=self.dbmycnf,user=self.dbuser,passwd=self.dbpasswd,sockfile=self.dbsock)
        backupcmd.execBackupFull(backdatadir)

    def backupIncrement(self, base):
        # 目录名组成：备份目录 + 周数 + incre + 周几增量 + 当前时间
        backdatadir = self.bakdir + Timer.getWeeks() + "_incre-" + str(Timer.getWday())  + "_" + Timer.getDate()
        # print base

        backupcmd = CommandExecuter(xtra="/bin/xtrabackup", cnf=self.dbmycnf, user=self.dbuser, passwd=self.dbpasswd,sockfile=self.dbsock)
        backupcmd.execBackupIncre(backdatadir,base)

def main():
    logfile = MariaBackup.apphome + "/log/" + Timer.getDate() + ".log"
    loger = Logerer("MariaBackup", logfile).getLoger()

    mback = MariaBackup()
    fact = FileAction()
    fact.mkDir(mback.bakdir)

    """ 备份 """
    # Timer.getWday返回周一为0,为保持同步+1
    wday = Timer.getWday() + 1
    #没有全备时先进行全备份
    if not mback.existFullbackup(mback.bakdir):
       # print "来全备"
        mback.backupFull()
    elif wday == 1:
       # print "已有全备"
        pass
    elif wday == 2 and not mback.existIncrebackup(mback.bakdir):
       # print "备周一数据"
        basedir = fact.getFulldir(mback.bakdir)
        mback.backupIncrement(mback.bakdir + basedir)
    elif wday > 2  and not mback.existIncrebackup(mback.bakdir):
       # print "其它备，周三至周日"
        basedir = fact.getIncrebase(mback.bakdir)
        if basedir is None:
            basedir = fact.getFulldir(mback.bakdir)
        mback.backupIncrement(mback.bakdir + basedir)

    """ 清除备份 """
    loger.info(fact.delDir(mback.bakdir,mback.bakkeep))


if __name__ == "__main__":
    main() 
