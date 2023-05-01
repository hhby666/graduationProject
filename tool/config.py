# -*- coding: utf-8 -*-

"""
Author:by wlq on 2023/4/17 20:05
FileName:config.py in CV_study
Tools:PyCharm python3.8.4
"""
mysql_config = {
    "host": "localhost",
    "port": 3306,
    "userName": "root",
    "password": "1248",
    "dbName": "face",
}
email_config = {
    "host": 'smtp.163.com',
    "license": 'IDRTDSYBFIHDBPNZ',
    "port": 25
}
re_dic = {
    "pwd": r"^.{6,32}$",
    "un": r"^[a-zA-Z0-9]{6,32}$",
    "email": r"^[A-Za-z0-9\u4e00-\u9fa5_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$",
    "name": r"^[A-Za-z0-9\u4e00-\u9fa5]+$",
    "sno": r"^[0-9]{6,10}$",
}
sign_dic = {
    0: "未签到",
    1: "已签到",
    2: "迟到"
}
sex_dic = {
    0: "男",
    1: "女",
    2: "其他"
}
