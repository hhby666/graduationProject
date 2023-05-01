# -*- coding: utf-8 -*-

"""
Author:by wlq on 2023/4/26 1:07
FileName:main.py in GraduationProject
Tools:PyCharm python3.8.4
"""
import sys

from PyQt5.QtWidgets import QApplication

from qt.mainThread import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())
