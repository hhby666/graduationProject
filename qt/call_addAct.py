# -*- coding: utf-8 -*-

"""
Author:by wlq on 2023/4/24 15:48
FileName:call_addAct.py in GraduationProject
Tools:PyCharm python3.9
"""
import sys
from datetime import *

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import *

from qt.module import MyMainWindow
from qt.ui.addAct import Ui_addAct
from tool.DBUtil import DBUtil, getDateTime


class AddAct(MyMainWindow, Ui_addAct):
    """"""
    addReturn = pyqtSignal()

    def __init__(self, parent=None):
        super(AddAct, self).__init__(parent)
        self.setupUi(self)
        self.initUi()
        self.initSlot()
        self.adminID = None
        self.initDT()

    def initUi(self):
        self.resize(460, 340)
        self.setFixedSize(460, 340)
        self.setWindowModality(Qt.ApplicationModal)
        self.name_le.setFocus()

    def initDT(self):
        self.start_dt.setMinimumDateTime(datetime.now())
        self.end_dt.setMinimumDateTime(datetime.now())
        self.end_dt.setDateTime(datetime.now() + timedelta(minutes=10))

    def initSlot(self):
        self.add_bt.clicked.connect(self.add)
        self.return_bt.clicked.connect(lambda: self.addReturn.emit())
        self.name_le.returnPressed.connect(lambda: self.add_bt.click())

    def add(self):
        name = self.name_le.text()
        st = self.start_dt.dateTime().toPyDateTime()
        ed = self.end_dt.dateTime().toPyDateTime()
        if name == "":
            QMessageBox.information(self, "waining", "活动名称不得为空！", QMessageBox.Ok)
            self.name_le.clear()
            self.name_le.setFocus()
            return
        db = DBUtil()
        res = db.save(f"insert into face.activity(name, admin_id, start_time, end_time) "
                      f"values('{name}', {self.adminID}, '{getDateTime(st)}', '{getDateTime(ed)}')")
        if res != 0:
            self.addReturn.emit()
        print(f'活动{name}已添加')
