# -*- coding: utf-8 -*-

"""
Author:by wlq on 2023/4/17 15:19
FileName:DBUtil.py in CV_study
Tools:PyCharm python3.8.4
"""
from datetime import datetime

import pymysql
from tool import config


def getDateTime(dt):
    dt = str(dt).split('.')[0]
    return datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')


class DBUtil:
    """mysql util"""
    db = None
    cursor = None

    def __init__(self):
        self.host = config.mysql_config['host']
        self.port = config.mysql_config['port']
        self.userName = config.mysql_config['userName']
        self.password = config.mysql_config['password']
        self.dbName = config.mysql_config['dbName']

    # 链接数据库
    def getCon(self):
        """ 获取connect """
        self.db = pymysql.Connect(
            host=self.host,
            port=self.port,
            user=self.userName,
            passwd=self.password,
            db=self.dbName
        )
        self.cursor = self.db.cursor()

    # 关闭链接
    def close(self):
        self.cursor.close()
        self.db.close()

    # 主键查询数据
    def getOne(self, sql):
        res = None
        try:
            self.getCon()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
        except Exception as e:
            print("查询失败！" + str(e))
        finally:
            self.close()
        return res

    # 查询列表数据
    def getAll(self, sql):
        res = None
        try:
            self.getCon()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
        except Exception as e:
            print("查询失败！" + str(e))
        finally:
            self.close()
        return res

    # 插入数据
    def __insert(self, sql):
        count = 0
        try:
            self.getCon()
            count = self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("操作失败！" + str(e))
            self.db.rollback()
        finally:
            self.close()
        return count

    # 保存数据
    def save(self, sql):
        return self.__insert(sql)

    # 更新数据
    def update(self, sql):
        return self.__insert(sql)

    # 删除数据
    def delete(self, sql):
        return self.__insert(sql)

