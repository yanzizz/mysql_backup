#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Project description
 __author__ = "chenqh"
 __date__: "2016/5/4"
 __company__: inno-view.cn
 __version__: "0.1"
 __note__: 脚本依赖percona-xtrabackup 2.3和rsync，请在使用前安装xtrabackup和rsync工具。
"""

import os
import re
import sys
import subprocess
from backup_config import BackupConfig

class MariaRestore(object):
    apphome = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
    def __init__(self, datadir="/data/dbbak", weeks=None, wday=None):
        bc = BackupConfig(MariaRestore.apphome + "/etc/config")
        self.datadir = datadir
        self.weeks = weeks
        self.wday = wday

        self.filelist = []
        self.resdst = bc.getResdata()

    """ 获取要恢复周的数据列表 """
    def getBacklist(self):
        allfile = os.listdir(self.datadir)

        for file in allfile:
            wmatch = re.match(self.weeks, file)
            if wmatch:
                self.filelist.append(file)
      #  print self.filelist
        return self.filelist

    def getFulldir(self):
        if self.filelist == []:
            print u"数据目录不存在，请检查源数据"
            sys.exit()
        for file in self.filelist:
            if re.search("full", file):
                return file


    def cmdExecute(self, cmd):
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (sout,serr) = p.communicate()
            #print "stdout:\n", sout
            #print "stderr:\n", serr
            if sout:
                print "STD:\n", sout

            if serr:
                print "ERR:\n", serr
        except OSError, ioe:
            print "Can't find file:" + self.command + "  or  " + self.cnf + "   or   " + self.dbsock
            print ioe
        except Exception, e:
            print e

    def restoreFull(self):
        self.getBacklist()
        fulldir = self.getFulldir()
        if self.filelist == []:
            print u"数据目录不存在，请检查源数据"
            sys.exit()

        # Perpare备份命令
        xtrcmd = ["/bin/xtrabackup", "--prepare", "--target-dir=" + self.datadir + "/" + fulldir]
        # 清空mysql data目录命令
        clscmd = ["rm", "-rf", self.resdst]
        # 恢复备份命令
        restcmd = ["/bin/rsync",
                  "-avzP",
                  "--exclude=backup-my.cnf",
                  "--exclude=xtrabackup_*",
                  self.datadir + "/" + fulldir + "/",
                  self.resdst]

        try:
            self.cmdExecute(xtrcmd)
        except Exception, e:
            print e
        else:
            os.system("service mysql stop")
            self.cmdExecute(clscmd)
            self.cmdExecute(restcmd)
            os.system("chown -R mysql:mysql " + self.resdst)
            os.system("service mysql start")

    def restoreIncrement(self):
        self.getBacklist()
        fulldir = self.getFulldir()

        print self.filelist
        #print fulldir
        if self.filelist == []:
            print u"数据目录不存在，请检查源数据"
            sys.exit()
        
        # Perpare full备份命令
        prefullcmd = ["/bin/xtrabackup", "--prepare", "--apply-log-only", "--target-dir=" + self.datadir + "/" + fulldir]

        # 取得增备的文件列表
        prelist = []
        for i in range(1,int(self.wday) + 1):
            patt = "incre-" + str(i)
            for file in self.filelist:
                wwmatch = re.search(patt, file)
                #print wwmatch
                if wwmatch:
                    prelist.append(file)

        precmdlist = []
        #print prelist
        # 生成增备的perpare命令列表
        for predir in prelist:
            precmdlist.append(["/bin/xtrabackup", "--prepare", "--apply-log-only", "--target-dir=" + self.datadir + "/" + fulldir, "--incremental-dir=" + self.datadir + "/" + predir])

        xtrcmd = ["/bin/xtrabackup", "--prepare", "--target-dir=" + self.datadir + "/" + fulldir]
        # 清空mysql data目录命令
        clscmd = ["rm", "-rf", self.resdst]
        # 恢复备份命令
        restcmd = ["/bin/rsync",
                  "-avzP",
                  "--exclude=backup-my.cnf",
                  "--exclude=xtrabackup_*",
                  self.datadir + "/" + fulldir + "/",
                  self.resdst]

        try:
            print "CMD:", prefullcmd
            self.cmdExecute(prefullcmd)

            for c in precmdlist:
                print "CMD:", c
                self.cmdExecute(c)

            print "CMD:", xtrcmd
            self.cmdExecute(xtrcmd)
        except Exception, e:
            print e
        else:
            os.system("service mysql stop")
            self.cmdExecute(clscmd)
            self.cmdExecute(restcmd)
            os.system("chown -R mysql:mysql " + self.resdst)
            os.system("service mysql start")


def main():
    def Useage():
      print "maria_restore.py <backupdir> <weeks> [wday]"
      print "\t backupdir       backupdata dir"
      print "\t weeks           week number of current year.(00 - 52)"
      print "\t wday            day of the week.(1 - 6)"


    global datadir, weeks, wday
    datadir, weeks, wday = None, None, None
    argnum = len(sys.argv)
    if argnum < 3:
        Useage()
        sys.exit(0)
    elif argnum == 3:
        datadir = sys.argv[1]
        weeks = sys.argv[2]
    elif argnum == 4:
        datadir = sys.argv[1]
        weeks = sys.argv[2]
        wday = sys.argv[3]

    if int(weeks) > 52:
        print "Error: please input correct weeks\t (00 - 52)"
        sys.exit(1)
    if wday is not None and int(wday) > 6:
        print "Error: please input correct day of the week\t (1-6)"
        sys.exit(1)

    mr = MariaRestore(datadir, weeks, wday)
    if wday is None:
        mr.restoreFull()
    else:
        mr.restoreIncrement()

if __name__ == "__main__":
    main() 
