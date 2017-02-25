#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/25 22:02
# @Author  : hale
# @Site    : 
# @File    : MyLog.py
# @Software: PyCharm

#-*-coding:utf8-*-
import logging
from datetime import datetime

class MyLog(object):
    def __init__(self):
        logging.basicConfig(level=logging.WARNING,
                format='%(asctime)s %(levelname)s\n%(message)s\n\n',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename= datetime.now().strftime("%Y%m%d%H%M%S") + '.log',
                filemode='a')

    def WriteLog(self, logContent):
        logging.info(logContent)

    def Error(self, errorContent):
        logging.error(errorContent)
