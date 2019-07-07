#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Project description
 __author__ = "chenqh"
 __date__: "2016/4/26"
 __company__: inno-view.cn
 __version__: "0.1"
 __note__: 脚本依赖percona-xtrabackup，请在使用前安装xtrabackup工具。
"""

import os
import subprocess
from logerer import Logerer
from timer import Timer

class CommandExecuter(object):
    apphome = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
    logger = Logerer("CommandExecuter", apphome + "/log/backuplog." + Timer.getDate()).getLoger()
    def __init__(self, xtra="/usr/bin/xtrabackup", cnf="/etc/my.cnf.d/server.cnf", user="root", passwd="", sockfile="/tmp/mysql.sock"):
        self.command = xtra
        self.cnf = cnf
        self.dbuser = user
        self.dbpass = passwd
        self.dbsock = sockfile

    def cmdExecute(self, cmd):
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            (sout,serr) = p.communicate()
            #print "stdout:\n", sout
            #print "stderr:\n", serr
            if sout:
                self.logger.info("STD:\n"+sout)

            if serr:
                self.logger.info("ERR:\n")
                self.logger.info(serr)
        except OSError, ioe:
            self.logger.info("Can't find file:" + self.command + "  or  " + self.cnf + "   or   " + self.dbsock)
            self.logger.info(ioe)
        except Exception, e:
            self.logger.info(e)

    def execBackupFull(self, bakdir):
        cmd = [self.command,
               "--defaults-file=" + self.cnf,
               "--user=" + self.dbuser,
               "--socket=" + self.dbsock,
               "--backup",
               "--target-dir=" + bakdir]
        if self.dbpass:
            cmd.append("--password=" + self.dbpass)
        #print "cmd:", cmd
        return self.cmdExecute(cmd)

    def execBackupIncre(self, bakdir, incredir):
        cmd = [self.command,
               "--defaults-file=" + self.cnf,
               "--user=" + self.dbuser,
               "--socket=" + self.dbsock,
               "--backup",
               "--target-dir=" + bakdir,
               "--incremental-basedir=" + incredir]
        if self.dbpass:
            cmd.append("--password=" + self.dbpass)
        return self.cmdExecute(cmd)

def main():
    loger = Logerer("MariaBackup", "../log/test.log").getLoger()

    cmd = ['/bin/xtrabackup', '--defaults-file=/etc/my.cnf.d/server.cnf', '--user=root', '--socket=/tmp/mysql.sock', '--backup', '--target-dir=/data/dbbak/20_full_2016-05-19_1721', '--password=123@abcd']
    ex = CommandExecuter()
    ex.cmdExecute(cmd)
    

if __name__ == "__main__":
    main()
