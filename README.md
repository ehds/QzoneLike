# 一 QzoneLike 功能介绍

    1. 急速点赞qq空间好友说说
    
    2. 好友说说邮箱提醒
    
    3.黑名单限制功能

# 二 使用说明

## 1.下载与安装
### 下载源码

    git clone https://github.com/Ds-Hale/QzoneLike.git
   
### 安装所需的库
1. requests库
    
```
pip install requests
```
2. selenium库
```
pip install -U selenium
```
3. phantomjs 

    到[phantomjs](http://phantomjs.org/download.html)下载,

    windows平台:把下载的文件拷贝到本地python环境中

    linux/mac平台:
    ```
    ln -s /where/is/phantomjs /usr/local/bin/phantomjs；
    ```
## 2.填写qzone_like目录下的config.conf 配置文件：

qq可以为用户自己的qq号，邮箱号
pwd 为用户登录密码
因为腾讯登录时长限制，所以将密码存储本地，以便cookies失效，自动登录(本应用不会以任何形式窃取用户隐私)
    

```
#用户的账号信息
[userinfo]
qq = ds_hale@qq.com
pwd = xxxxx
```


提示邮箱


```
[mail]
#邮箱提供商信息
pop_host = pop.sina.cn
smtp_host = smtp.sina.cn
#用户邮箱信息
username = hdddxwb@sina.cn
password = xxxxx
#接受者邮箱用于提示点赞消息
receiver = ds_hale@163.com,ds-hale@qq.com
```

黑名单设置
```

#不想点赞的黑名单
[blacklist]
QQ=1053600762,
nickname = hale,nickname
```



 ## 3 程序运行
 如果想要程序一直运行，建议运行在服务器上，这样不会错过任意时刻的还有动态
 填写完配置文件后
 只需进入qzone_like文件夹目录下
 
 windows下
```
python qzone_like.py
```

Linux

```
nohup python qzone_like.py &
```

注:
1. 本应用不会以任何形式保存窃取用户个人隐私
2. 由于腾讯方面可能会时常更换登录机制,导致功能失效,我会及时更改程序,如果有必要请及时更新
    
