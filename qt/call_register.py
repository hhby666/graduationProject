# -*- coding: utf-8 -*-

"""
Author:by wlq on 2023/4/19 10:56
FileName:call_login.py in GraduationProject
Tools:PyCharm python3.9
"""
import hashlib
import re
import sys

from PyQt5.QtCore import Qt, QRegExp, pyqtSignal
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import *

from qt.module import MyMainWindow
from qt.ui.register import Ui_register_window
from tool.DBUtil import DBUtil
from tool.config import re_dic


def getMD5(pwd):
    return hashlib.md5(pwd.encode('utf-8')).hexdigest()


class Register(MyMainWindow, Ui_register_window):
    """"""
    # 自定义信号量
    successReg = pyqtSignal(str, str)
    returnReg = pyqtSignal()

    def __init__(self, parent=None):
        super(Register, self).__init__(parent)
        self.setupUi(self)
        self.initUi()
        self.initSlot()
        self.initValidator()

    def initUi(self):
        # 设置大小
        self.resize(560, 430)
        self.setFixedSize(560, 430)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)

        # 绑定快捷键
        self.return_bt.setShortcut('ESC')

    def initValidator(self):
        # 设置文本校验
        reg = QRegExp(re_dic["un"])
        regVal = QRegExpValidator()
        regVal.setRegExp(reg)
        self.un_le.setValidator(regVal)

        reg = QRegExp(re_dic["pwd"])
        regVal.setRegExp(reg)
        self.pwd_le.setValidator(regVal)
        self.confirm_le.setValidator(regVal)

        reg = QRegExp(re_dic["email"])
        regVal.setRegExp(reg)
        self.email_le.setValidator(regVal)

    def initSlot(self):
        # 设置槽与信号
        self.register_bt.clicked.connect(self.register)
        self.name_le.returnPressed.connect(lambda: self.un_le.setFocus())
        self.un_le.returnPressed.connect(lambda: self.pwd_le.setFocus())
        self.un_le.textEdited.connect(lambda: self.checkFormat(self.un_le, 'un'))
        self.pwd_le.returnPressed.connect(lambda: self.confirm_le.setFocus())
        self.pwd_le.textEdited.connect(lambda: self.checkFormat(self.pwd_le, 'pwd'))
        self.confirm_le.returnPressed.connect(lambda: self.email_le.setFocus())
        self.confirm_le.textEdited.connect(lambda: self.checkFormat(self.confirm_le, 'pwd'))
        self.email_le.returnPressed.connect(lambda: self.register_bt.click())
        self.email_le.textEdited.connect(lambda: self.checkFormat(self.email_le, 'email'))
        self.return_bt.clicked.connect(lambda: self.returnReg.emit())

    @staticmethod
    def checkFormat(le, type_str):
        if not check(re_dic[type_str], le.text()) and le.text() != "":
            le.setStyleSheet("background-color: red")
        else:
            le.setStyleSheet("background-color: white")

    def register(self):
        if self.warning(self.un_le, 'un', '帐号') or self.warning(self.pwd_le, 'pwd', '密码') or self.warning(
                self.confirm_le, 'pwd', '确认密码') or self.warning(self.email_le, 'email', '邮箱'):
            return
        name = self.name_le.text()
        user_name = self.un_le.text()
        pwd = self.pwd_le.text()
        pwd_confirm = self.confirm_le.text()
        email = self.email_le.text()
        if pwd != pwd_confirm:
            QMessageBox.information(self, "waining", "确认密码不正确", QMessageBox.Ok)
            self.confirm_le.setFocus()
            return
        db = DBUtil()
        res = db.getOne(f"select user_name from administrator where user_name='{user_name}'")
        if res is not None:
            QMessageBox.information(self, "waining", "帐号已存在！请重新注册！", QMessageBox.Ok)
            self.un_le.clear()
            self.un_le.setFocus()
            return
        res = db.save(
            f"insert into administrator(name, user_name, password, email) values('{name}',"
            f" '{user_name}','{getMD5(pwd)}', '{email}')")
        if res != 0:
            self.successReg[str, str].emit(user_name, pwd)

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


def check(re_str, text):
    if re.match(re_str, text) is None:
        return False
    else:
        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Register()
    w.show()
    sys.exit(app.exec())
