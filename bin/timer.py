#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Project description
 __author__ = "chenqh"
 __date__: "2016/4/25"
 __company__: inno-view.cn
 __version__: "0.1"
 __see__: 参考
"""

import time
from datetime import date,datetime

class Timer(object):
    @staticmethod
    def getDate():
	return time.strftime("%Y-%m-%d_%H%M",time.localtime())

    @staticmethod
    def getWeeks():
	# 返回当前日在一年中的第几周
	return time.strftime("%W")

    @staticmethod
    def getWday():
	# 返回当前日在一周中的第几天,周一为0
	wday = datetime.weekday(date.today())
	#wday = time.strftime("%w")
	return int(wday)

def main():
    dtime = Timer.getDate()
    print(dtime)

#    print int(Timer.getWeeks()) - 4

    print(Timer.getWday())

if __name__ == "__main__":
    main()
