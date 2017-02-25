#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/25 22:02
# @Author  : hale
# @Site    : 
# @File    : MyLog.py
# @Software: PyCharm

#-*-coding:utf8-*-
from setuptools import setup

setup(
    name='qzonelike',
    version='0.1',
    license='MIT',
    author_email='grephale@gmail.com',
    url='https://github.com/Ds-Hale/QzoneLike',
    description='Python QQZone',
    platforms=['any'],
    py_modules= ['qzone_like'],
    packages= ['qzone_like'],
    install_requires=['requests'],
    include_package_data=True,
)
