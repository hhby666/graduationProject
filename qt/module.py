# -*- coding: utf-8 -*-

"""
Author:by wlq on 2023/4/21 1:09
FileName:module.py in GraduationProject
Tools:PyCharm python3.9
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *


class MyMainWindow(QMainWindow, QWidget):
    """"""

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.myInit()

    def myInit(self):
        # 设置图标
        self.setWindowIcon(QIcon("C:/Project/PythonProject/GraduationProject/resources/ico.png"))
        self.setWindowModality(Qt.ApplicationModal)
        # 设置居中
        self.center()

        # 设置基础样式
        self.setStyleSheet("* {font-family: 'YaHei Monaco Hybird'; font-size: 12pt; background-color: white}")
        self.setStyleSheet("QPushButton {background-color: skyblue;}")

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))
