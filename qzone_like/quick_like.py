#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/25 17:20
# @Author  : hale
# @Site    : 
# @File    : quick_like.py
# @Software: PyCharm
from selenium import webdriver
import sys
# 引入配置对象DesiredCapabilities
from util import *
import threading
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from MyLog import  MyLog
global driver
headers = {"User-Agent":"Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"}
post = {"appid": "311", "format": "purejson","opr_type": "like"}
myLog = None
CurInfo = None

class Current:
    def __init__(self):
        self.current = 0
        self.donot_like_qq = get_black_num("QQ")
        self.donot_like = get_black_num("nickname")
    def large_current(self,current):
        if current>self.current:
            self.current = current
            print "T"
            return True
        else:
            print "F"
            return False

    def is_black(self,nickname='', qq=''):
        """
        nickname : QQ nickname
        qq : the QQ number
        """
        #every time get the black list from config in case the config is changed
        return True if nickname in self.donot_like or qq in self.donot_like_qq else False
# only init driver once during process is running

def initDriver():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (headers["User-Agent"])
    dcap["phantomjs.page.settings.loadImages"] = False
    return webdriver.PhantomJS(desired_capabilities=dcap)

def UpdateNews(subject,content):

    #myLog.WriteLog(content)
    try:
        from SendMail import SendMail
        Mail = SendMail()
        if "error" in content:
            Mail.send_mail(subject,get_mail_receiver(),content)
        else:
            Mail.send_HTML(subject,get_mail_receiver(),content)
    except:
        myLog.Error("Send Mail Error")
#Get userinfo from config file
def getUserInfo(config):
    configFile = os.path.join(sys.path[0], config)
    cReader = ConfigParser.ConfigParser()
    cReader.read(configFile)
    return cReader.get("userinfo","qq"),cReader.get("userinfo","pwd")

#When cookie is not useful，re-login!
def ChangeCookie():
    print "change"
    user, pwd = getUserInfo("config.conf")
    cookie = {}
    driver = initDriver()
    while True:
        qzone_login_url = "http://qzone.qq.com"
        driver.get(qzone_login_url)
        myLog.Error("Enter Login Page")
        try:
            access = driver.find_element_by_id('guideSkip')  # 继续访问触屏版按钮
            access.click()
            myLog.Error("Click guideSkip button")
            time.sleep(1)
        except Exception, e:
            myLog.Error("Cannot Click guide button")
            time.sleep(3)
        account_input = driver.find_element_by_id('u')  # 账号输入框
        password_input = driver.find_element_by_id('p')  # 密码输入框
        go = driver.find_element_by_id('go')  # 登录按钮
        account_input.clear()
        password_input.clear()
        account_input.send_keys(user)
        password_input.send_keys(pwd)
        go.click()
        myLog.Error("Input QQ and Password，click Login button ")
        time.sleep(2)
        try:
            for elem in driver.get_cookies():
                cookie[elem['name']] = elem['value']
            myLog.WriteLog('Get the cookie of QQ:{qq} successfully!(共{num}个键值对\n{cookie}:'.format(qq=cookie["uin"], num=len(cookie),cookie=cookie))
            driver.quit()
            myLog.Error("quick Login Model")
            saveCookie(content=str(cookie))
            break
        except:
            myLog.Error("Login Error")
            time.sleep(10)

    return cookie

def cookiedict2str(cookie):
    #方便request使用{"Cookies":"***"}
    cookie_str = ""
    for name in cookie:
        each = "{name}={value};".format(name=name, value=cookie[name])
        cookie_str += each
    cookie_str = cookie_str.replace('\r', '')
    return {"Cookies":cookie_str}
def getCookiesAndGtk(cookie):
    try:
        cookies = cookiedict2str(cookie)
        if cookie.has_key("p_skey"):
            gtk = getGtk(cookie["p_skey"])
        else:
            gtk = getGtk(cookie["skey"])
    except:
        cookies=gtk=""
    return cookies,gtk
def quick_like(cookie={}):
    cookie = getCookieFromFile()
    cookies, gtk= getCookiesAndGtk(cookie)
    try_count=0
    feed = {}
    while True:
        try:
            active_url = "https://h5.qzone.qq.com/webapp/json/mqzone_feeds/getActiveFeeds?g_tk=" + str(gtk)
            res = requests.get(active_url, cookies=cookies, headers=headers)
            data = json.loads(res.text, encoding="utf-8")
            feed = data["data"]['vFeeds'][0] #the first element
        except:
            try_count+=1
            #设定尝试次数为3,防止网络波动造成错误判断cookie失效
            if (try_count>3):
                cookie = ChangeCookie()
                cookies, gtk=getCookiesAndGtk(cookie)
                try_count=0
                pass
            time.sleep(2)
            continue
        current = feed["userinfo"]["user"]["timestamp"]
        if (CurInfo.large_current(current)):
            uin = feed["userinfo"]["user"]["uid"].encode("utf-8")
            nickname = feed["userinfo"]["user"]["nickname"].encode("utf-8")
            if(not CurInfo.is_black(nickname, uin)):
                print "true"
                post["opuin"] = uin
                post["curkey"] = feed["comm"]["curlikekey"]
                post["unikey"] = feed["comm"]["curlikekey"]
                like_url = "https://h5.qzone.qq.com/proxy/domain/w.qzone.qq.com/cgi-bin/likes/internal_dolike_app?g_tk=" + str(gtk)
                for i in range(3):
                    try:
                        res = requests.post(like_url, data=post, cookies=cookies)
                        print res.content
                        if "succ" in res.content:
                            HTML = parseToHtml(feed)
                            send_mail_thread = threading.Thread(target=UpdateNews, args=(nickname,HTML))
                            send_mail_thread.setDaemon(True)
                            send_mail_thread.setName("send mail thread")
                            send_mail_thread.start()
                            break
                    except:
                        continue
        time.sleep(3)

if __name__ == "__main__":
    myLog = MyLog()
    CurInfo = Current()
    # quick_thread = threading.Thread(target=quick_like, args=({}))
    # quick_thread.setDaemon(True)
    # quick_thread.start()
    # quick_thread.join()
    # UpdateNews("Qzone Like error", "system error")
    ChangeCookie()
    # cookies,gtk =getCookiesAndGtk(getCookieFromFile())
    # print cookies
    # active_url = "https://h5.qzone.qq.com/webapp/json/mqzone_feeds/getActiveFeeds?g_tk=" + str(gtk)
    # res = requests.get(active_url, cookies=cookies, headers=headers)
    # print res.content