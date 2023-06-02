# -*- coding: utf-8 -*-

"""
Author:by wlq on 2023/5/10 10:43
FileName:call_manageUser.py in GraduationProject
Tools:PyCharm python3.8.4
"""
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import *

from qt.module import MyMainWindow
from qt.ui.manageUser import Ui_manageUser
from tool.DBUtil import DBUtil


class ManageUser(MyMainWindow, Ui_manageUser):
    """"""

    def __init__(self, adminID, parent=None):
        super(ManageUser, self).__init__(parent)
        self.setupUi(self)
        self.adminID = adminID
        self.initUi()
        self.initSlot()
        self.initTable()

    def initUi(self):
        self.setWindowModality(Qt.ApplicationModal)

    def initSlot(self):
        self.return_bt.clicked.connect(self.close)
        self.delete_btn.clicked.connect(self.delete)

    def delete(self):
        items = self.user_tb.selectedItems()
        db = DBUtil()
        for i in range(0, len(items), 3):
            uid = items[i].text()
            print(f"uid:{uid}")
            sql = f"delete from face.user where id = {uid}"
            db.delete(sql)
        self.initTable()

    def initTable(self):
        self.user_tb.setColumnCount(3)
        self.user_tb.setHorizontalHeaderLabels(["id", "学号", "姓名"])
        self.user_tb.setSelectionMode(3)
        self.user_tb.setSelectionBehavior(1)
        self.user_tb.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_tb.setEditTriggers(QAbstractItemView.NoEditTriggers)
        datas = self.getUserData()
        print(f"data lens:{len(datas)}")
        self.user_tb.setRowCount(len(datas))
        for i in range(len(datas)):
            item0 = QTableWidgetItem(str(datas[i][0]))
            item0.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.user_tb.setItem(i, 0, item0)
            item1 = QTableWidgetItem(datas[i][1])
            item1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.user_tb.setItem(i, 1, item1)
            item2 = QTableWidgetItem(datas[i][2])
            item2.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.user_tb.setItem(i, 2, item2)

    def getUserData(self):
        db = DBUtil()
        sql = f"""select u.id, u.sno, u.name
                    from face.user u
                    where u.admin_id = {self.adminID}"""
        res = db.getAll(sql)
        return res
