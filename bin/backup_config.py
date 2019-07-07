#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Project description
 __author__ = "chenqh"
 __date__: "2016/4/25"
 __company__: inno-view.cn
 __version__: "0.1"
 __see__: 参考
"""
import ConfigParser
import sys

class BackupConfig(object):
    def __init__(self,confile):
        self.confile = confile
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.confile)

        self.dbhost = None
        self.dbport = None
        self.dbuser = None
        self.dbpasswd = None
        self.dbsock = None
        self.mycnf = None
        self.bakdatadir = None
        self.bakkeepcycles = None

        self.resdata = None

# ''' ----  test section ---
#     def getConf(self):
#         config = ConfigParser.ConfigParser()
#         config.read(self.confile)
#         try:
#             for item in config.options("bakconf"):
#                 # print item
#                 for val in item:
#                     val = config.get("bakconf", item)
#                 print(item + "=" + val)
#         except ConfigParser.NoSectionError, e:
#             print(e)
#             sys.exit(1)
#
#     def getConfig(self):
#         for sec in self.config.sections():
#             print("[" + sec + "]")
#             for item in self.config.options(sec):
#                 for val in item:
#                     val = self.config.get(sec,item)
#                 print(item + "=" + val)
# '''
    def getHost(self):
        self.dbhost = self.config.get("db","dbhost")
        return self.dbhost

    def getPort(self):
        self.dbport = self.config.get("db","dbport")
        return self.dbport

    def getUser(self):
        self.dbuser = self.config.get("db","dbuser")
        return self.dbuser

    def getPasswd(self):
        self.dbpasswd = self.config.get("db","dbpasswd")
        return self.dbpasswd

    def getSocket(self):
        self.dbsock = self.config.get("db","dbsock")
        return self.dbsock

    def getMycnf(self):
        self.mycnf = self.config.get("db","mycnf")
        return self.mycnf

    def getBakdir(self):
        self.bakdatadir = self.config.get("backup","bakdatadir")
        return self.bakdatadir

    def getBakkeep(self):
        self.bakkeepcycles = self.config.get("backup","keepcycles")
        return self.bakkeepcycles

    def getResdata(self):
        self.resdata = self.config.get("restore","resdatadir")
        return self.resdata

def main():
    bc = BackupConfig("../etc/config")
    # bc.getConfig()
    print(bc.bakdatadir)
    bc.getBakdir()
    print(bc.bakdatadir)

    print bc.getResdata()
    print bc.getResredo()


if __name__ == "__main__":
    main()    
