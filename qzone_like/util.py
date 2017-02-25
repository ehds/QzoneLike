# -*- coding:utf-8 -*-
import os
import time
import random
import cookielib
import requests
import json
import ConfigParser
mgList_url = 'https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/' \
             'emotion_cgi_msglist_v6?ftype=0&sort=0&pos=0&num=20&replynum=100' \
             '&callback=_preloadCallback&code_version=1&format=jsonp&need_private_comment=1'
qr_refresh_url = 'http://ptlogin2.qq.com/ptqrshow?appid=549000912&e=2&l=M&s=3&d=72&v=4&daid=5'
check_login_url = 'http://ptlogin2.qq.com/ptqrlogin?u1=http%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&js_ver=10168&js_type=1&login_sig=&pt_uistyle=40&aid=549000912&daid=5&'
def get_current_gTk(cookie_file='cookie.txt'):
    cookie = cookielib.MozillaCookieJar()
    cookie.load(cookie_file, ignore_discard=True)
    p_skey = cookie._cookies['.qzone.qq.com']['/']['p_skey'].value
    g_tk = getGtk(p_skey)
    return str(g_tk)

def get_current_uin(cookie_file='cookie.txt'):
    cookie = cookielib.MozillaCookieJar()
    cookie.load(cookie_file, ignore_discard=True)
    qq_uin = cookie._cookies['.qq.com']['/']['uin'].value[1:]
    return qq_uin
def get_qr_url():
    random = get_random()
    return str(qr_refresh_url+'&t='+str(random))

def getGtk(string):
    hash = 5381
    for i in string:
        hash += (hash<<5)+ord(i)
    return hash & 0x7fffffff

def get_timestamp():
    """
    :return: 13 timestamp
    """
    return int(time.time()*1000)

def timestamp_to_date(timestamp):
    timestamp = int(timestamp)
    timearray = time.localtime(timestamp)
    timestr = time.strftime("%Y-%m-%d %H:%M:%S",timearray)
    return timestr

def get_random():
    """
       :return: random
       """
    return random.random()

def get_check_login_url():

    return str(check_login_url+'action=0-0-'+str(get_timestamp())+'&')

def cookiejar_to_cookiestr(cookie_file='cookie.txt'):
    """

    :param cookie_file: cookie file path
    :return: a dict of cookies
    """

    cookie = cookielib.MozillaCookieJar()
    try:
        cookie.load(cookie_file, ignore_discard=True)

    except:

        pass
    cookies_dict= {}
    cookie_str = ''
    for item in cookie:
        cookie_str+=item.name+'='+item.value+'; '
    cookie_str = cookie_str.replace('\r','')
    cookies_dict['Cookies']=cookie_str
    return cookies_dict

def get_black_num(type='QQ',config_file='config.conf'):
    cf = ConfigParser.ConfigParser()
    cf.read(config_file)
    blacklist = cf.get('blacklist',type)
    return blacklist.split(',')

def get_mail_receiver(config_file="config.conf"):
    cf = ConfigParser.ConfigParser()
    cf.read(config_file)
    blacklist = cf.get('mail', "receiver")
    return blacklist.split(',')

def print_qrcode(file = 'qr.png'):
    # 为了简化，作为测试，像素大小已经测量
    im = Image.open(file)
    box = (6, 6, 105, 105)
    im = im.crop(box)  # 截取二维码正文
    im = im.resize((198, 198))  # 将尺寸放大

    # im.save('qr_copy.png')
    # im.show()
    def get_pixel(i, j):
        return im.getpixel((i * 6 + 3, j * 6 + 3))  # 获取每个格子的中间的像素值。似乎返回值为一个整数

    code = ''
    print get_pixel(32, 31)
    # 图片是一个33x33的二维码
    for j in range(33):
        for i in range(33):
            if get_pixel(i, j) == 255:
                code += '　'
            else:
                code += '▇'
        print '     ' + code + '\r'
        code = ''
#print_qrcode()
def parseProfileToHtml(profileJson):
    # Change profile(json) into html
    html = """<div class="container">"""
    #extract summary
    try:
        summary = profileJson["summary"]["summary"].encode("utf-8")
        html +="<p>"+summary+"<p>"

    except:
        summary = ""
        #if there are pics
    if profileJson.has_key("pic"):
        b= profileJson["pic"]["picdata"]
        for item in b:
            img_url = item["photourl"]["0"]["url"]
            html+="""<img src={src}></img><a href="{src}">click to see</a>""".format(src=img_url)
    if profileJson.has_key("video"):
        video = str(profileJson["video"]["videourl"].encode("utf-8"))
        html += """<video src="{src}" controls="controls" width="100%"></video><a href="{src}">click to see</a>""".format(src=video)
    html+="</div>"
    return html
"""
"""
def parseUserInfoToHtml(UserInfoJson):
    html = """<div class="head"><div id="avator">
                <img src="{avator}"></div>
                <div class="info">
                <p>{name}</p>
                <p>{time}</p>
                </div>
            </div>"""
    user = UserInfoJson["userinfo"]["user"]
    uin = user["uin"]
    userImageUrl = "https://qlogo3.store.qq.com/qzone/{uin}/{uin}/100".format(uin=uin)
    nickname = user["nickname"].encode("utf-8")
    time = timestamp_to_date(user["timestamp"]).encode("utf-8")
    return html.format(avator=str(userImageUrl),name = str(nickname),time=str(time))
def parseToHtml(content):
    try:
        HTML =parseUserInfoToHtml(content)+parseProfileToHtml(content)
    except:
        HTML = "PARSE error"
    return  HTML
def saveCookie(file="cookie.txt",content="cookie"):
    with open(file,"w") as f:
        f.write(content)
        f.flush()
        f.close()

def getCookieFromFile(file="cookie.txt"):
    if os.path.exists("./cookie.txt"):
        with open (file,"r") as f:
            try:
                return eval(f.read())
                f.close()
            except:
                return {}
    else:
        return {}

