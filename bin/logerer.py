#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""参考 description
 __author__ = "chenqh"
 __date__: "2016/4/29"
 __company__: inno-view.cn
 __version__: "0.1"
 __note__: 参考
"""

import logging

class Logerer(object):
    ''' 类初始化方法 '''
    def __init__(self, logname, logfile):
        self.logname = logname
        self.logfile = logfile

    def getLoger(self):
        self.logger = logging.getLogger(self.logname)
        self.logger.setLevel(logging.INFO)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(self.logfile)
        fh.setLevel(logging.INFO)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # 定义handler的输出格式
        # fmt = "%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s"
        fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(fmt)
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        self.logger.addHandler(fh)
        #self.logger.addHandler(ch)
        #返回logger
        return self.logger

def main():
    loger = Logerer("test","test.txt")
    l = loger.getLoger()
    l.info("llk辊迷遥一")

if __name__ == "__main__":
    main()    
