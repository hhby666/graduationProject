# -*- coding: utf-8 -*-

"""
Author:by wlq on 2023/4/19 10:56
FileName:call_login.py in GraduationProject
Tools:PyCharm python3.9
"""
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *

from qt.call_register import getMD5, Register
from qt.module import MyMainWindow
from qt.ui.login import Ui_MainWindow_Login
from tool.DBUtil import DBUtil


class Login(MyMainWindow, Ui_MainWindow_Login):
    """"""
    successLogin = pyqtSignal(int)

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.register = Register()
        self.setupUi(self)
        self.initUi()
        self.initSlot()

    def initUi(self):
        self.resize(500, 430)
        self.setFixedSize(500, 430)
        self.un_le.setFocus()
        self.un_le.setPlaceholderText("请输入账号")
        self.pwd_le.setPlaceholderText("请输入密码")
        self.login_bt.clicked.connect(self.login)
        self.quit_bt.setShortcut('ESC')

    def initSlot(self):
        self.un_le.returnPressed.connect(lambda: self.pwd_le.setFocus())
        self.pwd_le.returnPressed.connect(lambda: self.login_bt.click())
        self.register_bt.clicked.connect(self.openRegister)
        self.register.successReg.connect(self.registerSuccess)
        self.register.returnReg.connect(self.returnLogin)

    def login(self):
        user_name = self.un_le.text()
        pwd = getMD5(self.pwd_le.text())
        if user_name == '':
            QMessageBox.information(self, "waining", "帐号不能为空", QMessageBox.Ok)
            self.un_le.setFocus()
            return
        if pwd == getMD5(""):
            QMessageBox.information(self, "waining", "密码不能为空", QMessageBox.Ok)
            self.pwd_le.setFocus()
            return
        db = DBUtil()
        res = db.getOne(f"select a.password, a.id from face.administrator a where a.user_name='{user_name}'")
        if res is None:
            QMessageBox.information(self, "waining", "账号不存在", QMessageBox.Ok)
            self.un_le.setText("")
            self.pwd_le.setText("")
            self.un_le.setFocus()
            return
        else:
            if res[0] == pwd:
                print(f"{user_name}登录成功!")
                self.destroy()
                self.successLogin.emit(res[1])
                return
            else:
                QMessageBox.information(self, "waining", "密码错误", QMessageBox.Ok)
                self.pwd_le.setText("")
                self.pwd_le.setFocus()
                return

    def openRegister(self):
        self.register.show()
        self.close()

    def registerSuccess(self, un, pwd):
        self.show()
        self.register.destroy()
        self.un_le.setText(un)
        self.pwd_le.setText(pwd)
        QMessageBox.information(self, "tips", "注册成功请登录！", QMessageBox.Ok)
        self.pwd_le.setFocus()

    def returnLogin(self):
        self.register.destroy()
        self.show()
        self.un_le.setFocus()
