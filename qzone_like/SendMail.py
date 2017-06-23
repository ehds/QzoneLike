#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/25 21:45
# @Author  : hale
# @Site    : 
# @File    : SendMail.py
# @Software: PyCharm

# -*- coding:utf-8 -*-
import smtplib
import os
import sys
import time
from util import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import ConfigParser

class configReader(object):
    def __init__(self, configPath):
        configFile = os.path.join(sys.path[0],configPath)
        self.cReader = ConfigParser.ConfigParser()
        self.cReader.read(configFile)

    def readConfig(self, section, item):
        return self.cReader.get(section, item)
"""
简单发送邮件程序
首先得在config里面填写相关信息
[mail]
pop_host = pop.sina.cn
smtp_host = smtp.sina.cn
port = 25
username = user
password = pwd
"""
class SendMail():
    _CONFIGPATH = 'config.conf'
    def __init__(self):
        cf = configReader(self._CONFIGPATH)
        self.host = cf.readConfig('mail','smtp_host')
        self.port = cf.readConfig('mail','port')
        self.username = cf.readConfig('mail','username')
        self.password = cf.readConfig('mail','password')
        self.login()

    def login(self):
        try:
            self.mail_handle = smtplib.SMTP(self.host, self.port)
            self.mail_handle.login(self.username, self.password)

        except:
            print 'failed to login'

    def send_mail(self,subject, to_list, content='Success'):
    	"""
		@subject : the subject of the mail
		@to_list : the list of receiver's email address
		@content : what you would want to send
    	"""
        msg = MIMEText(content,_subtype='plain',_charset='utf-8')
        me = subject+'<'+self.username+'>'
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            self.mail_handle.sendmail(me, to_list, msg.as_string())
        except:
            print 'failed to send mail'
        self.mail_handle.close()
    def send_HTML(self,subject,to_list,content):
        msg = MIMEMultipart('alternatvie')
        me = subject + '<' + self.username + '>'
        msg['Subject'] =subject # 组装信头
        msg['From'] =me # 使用国际化编码
        msg['To'] = ";".join(to_list)

        html = open('show.html').read() # 读取HTML模板
        html+=content+"</body></html>"
        print html
        html_part = MIMEText(html, 'html')  # 实例化为html部分
        html_part.set_charset('utf-8')  # 设置编码
        msg.attach(html_part)  # 绑定到message里
        try:
            self.mail_handle.sendmail(me, to_list, msg.as_string())
        except:
            print 'failed to send mail'
        self.mail_handle.close()
if __name__  == "__main__":
    Mail = SendMail()
    Mail.send_HTML("test",["ds_hale@163.com"],"test")