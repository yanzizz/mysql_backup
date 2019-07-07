#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 文件目录相关操作
 __author__ = "chenqh"
 __date__: "2016/4/25"
 __company__: inno-view.cn
 __version__: "0.1"
 __see__: 参考
"""
import os
import re
import shutil

from logerer import Logerer
from timer import Timer


class FileAction(object):
    apphome = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
    logger = Logerer("FileAction", apphome + "/log/" + Timer.getDate() + ".log").getLoger()

    def __init__(self):
        self.currdir = os.getcwd()

    def getDirlist(self, path=None):
        if path is None:
            self.dlist = os.listdir(self.currdir)
        else:
            self.dlist = os.listdir(path)
        return self.dlist

    def mkDir(self, path):
        if os.path.exists(path):
            # print(path + "already exist!")
            self.logger.info(path + "already exist!")
        else:
            try:
                os.mkdir(path)
            except IOError, ex:
                self.logger.info(ex)

    """ 取得本周的全备目录名 """

    def getFulldir(self, path):
        allfile = self.getDirlist(path)
        # print allfile

        # 取得本周的目录列表
        filelist = []
        for f in allfile:
            wmatch = re.match(Timer.getWeeks(), f)
            # print match
            if wmatch:
                filelist.append(f)

        # 取得本周的全备目录名
        for f in filelist:
            # print re.match(Timer.getWday(), file)
            if re.search("full", f):
                return f

    """ 取得昨天的增备目录名 """

    def getIncredir(self, path):
        allfile = self.getDirlist(path)
        # print allfile

        # 取得本周的目录列表
        filelist = []
        for f in allfile:
            wmatch = re.match(Timer.getWeeks(), f)
            # print match
            if wmatch:
                filelist.append(f)

        # 取得昨天备份的目录名，按星期数来取，周一为0，周二为1 .... 因周日数据为全备，故没有incre-0
        patt = "incre-" + str(Timer.getWday())
        # print "file_action:" + patt
        for f in filelist:
            wwmatch = re.search(patt, f)
            # print wwmatch
            if wwmatch:
                # print wwmatch.group()
                return f

    """ 取得增备的BASE目录名 (实际周数为前天)"""

    def getIncrebase(self, path):
        allfile = self.getDirlist(path)
        # print allfile

        # 取得本周的目录列表
        filelist = []
        for f in allfile:
            wmatch = re.match(Timer.getWeeks(), f)
            # print match
            if wmatch:
                filelist.append(f)

        # 取得增备的目录名，按星期数来取，备昨天的数据，BASE为前天，故-2
        patt = "incre-" + str(Timer.getWday() - 1)
        # print "file_action:" + patt
        for f in filelist:
            wwmatch = re.search(patt, f)
            # print wwmatch
            if wwmatch:
                # print wwmatch.group()
                return f

    """ 删除保留周之前的数据 """

    def delDir(self, path, keepweek):
        allfile = self.getDirlist(path)
        # print allfile
        # 取得要删除的文件夹列表
        dellist = []
        delweeks = int(Timer.getWeeks()) - int(keepweek)
        for f in allfile:
            for wn in range(delweeks):
                wn = wn + 1
                wmatch = re.match(str(wn).zfill(2) + "_", f)
                if wmatch:
                    dellist.append(f)
        # print dellist

        # 删除文件
        try:
            for f in dellist:
                shutil.rmtree(path + "/" + f)
            self.logger.info("Delete files:" + ",".join(dellist))
        except Exception as e:
            self.logger.error(e)

def main():
    fa = FileAction()

    # fa.getDirlist("d:/data/")
    # # print(fa.currdir)
    # print(fa.dlist)

    # fa.mkDir("e:/data")
    # print fa.getFulldir("e:/data/dbbak")
    print fa.getIncredir("/data/dbbak")

    # fa.delDir("e:/data/dbbak",4)


if __name__ == "__main__":
    main()
