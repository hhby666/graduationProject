# -*- coding: utf-8 -*-

"""
Author:by wlq on 2023/4/23 22:32
FileName:call_addUser.py in GraduationProject
Tools:PyCharm python3.9
"""
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import *

from qt.call_register import check
from qt.module import MyMainWindow
from qt.ui.addUser import Ui_add_user
from tool.DBUtil import DBUtil
from tool.config import re_dic


class AddUser(MyMainWindow, Ui_add_user):
    """"""
    addReturn = pyqtSignal()

    def __init__(self, adminID, actID, parent=None):
        super(AddUser, self).__init__(parent)
        self.setupUi(self)
        self.initUi()
        self.initSlot()
        self.adminID = adminID
        self.actID = actID
        self.feature = None

    def initUi(self):
        self.resize(1200, 600)
        self.setFixedSize(1200, 600)
        self.setWindowModality(Qt.ApplicationModal)
        self.name_le.setFocus()

    def initSlot(self):
        self.add_bt.clicked.connect(self.add)
        self.return_bt.clicked.connect(lambda: self.addReturn.emit())

        self.name_le.returnPressed.connect(lambda: self.sno_le.setFocus())
        self.sno_le.returnPressed.connect(lambda: self.email_le.setFocus())
        self.email_le.returnPressed.connect(lambda: self.add_bt.click())

    def add(self):
        if self.feature is None:
            QMessageBox.information(self, "waining", "人脸特征提取识败请重新录入!", QMessageBox.Ok)
            self.addReturn.emit()
        if self.warning(self.name_le, 'name', '姓名') or self.warning(self.sno_le, 'sno', '学号') \
                or self.warning(self.email_le, 'email', '邮箱'):
            return
        name = self.name_le.text()
        sno = self.sno_le.text()
        email = self.email_le.text()
        db = DBUtil()
        res = db.getOne(f"select sno from face.user where sno='{sno}'")
        if res is not None:
            QMessageBox.information(self, "waining", "学号已存在！请重新填写！", QMessageBox.Ok)
            self.sno_le.clear()
            self.sno_le.setFocus()
            return
        feature = self.feature2str()
        res = db.save(
            f"insert into face.user(name, sno, sex, email, feature, admin_id) values('{name}',"
            f" '{sno}', {self.getSex()} , '{email}', '{feature}', {self.adminID})")
        if res != 0:
            print(f"{name}已经录入")
            id = db.getOne(f"select id from face.user where sno = '{sno}'")[0]
            db.save(f"insert into face.sign(user_id, activity_id) values({id}, {self.actID})")
            self.addReturn.emit()

    def warning(self, le, type_str, name):
        text = le.text()
        if text == "":
            QMessageBox.information(self, "waining", f"{name}不能为空", QMessageBox.Ok)
            le.setFocus()
            return True
        elif not check(re_dic[type_str], text):
            QMessageBox.information(self, "waining", f"{name}格式不正确", QMessageBox.Ok)
            le.setFocus()
            return True
        else:
            return False

    def getSex(self):
        if self.man_rb.isChecked():
            return 0
        else:
            return 1

    def feature2str(self):
        # 将numpy array类型转化为列表
        encoding_array_list = self.feature.tolist()
        # 将列表里的元素转化为字符串
        encoding_str_list = [str(i) for i in encoding_array_list]
        # 拼接列表里的字符串
        encoding_str = ','.join(encoding_str_list)
        return encoding_str
