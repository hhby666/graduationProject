# -*- coding: utf-8 -*-

"""
Author:by wlq on 2023/4/24 23:48
FileName:call_manageAct.py in GraduationProject
Tools:PyCharm python3.9
"""
import csv
import pathlib
from datetime import datetime

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import *

from qt.module import MyMainWindow
from qt.ui.addUserToAct import Ui_addUser
from qt.ui.manageAct import Ui_manageAct
from tool import config
from tool.DBUtil import DBUtil, getDateTime


class ManageAct(MyMainWindow, Ui_manageAct):
    manageReturn = pyqtSignal(list)
    changeSubmit = pyqtSignal(list)
    deleteSignal = pyqtSignal()

    def __init__(self, adminID, actID, act, parent=None):
        super(ManageAct, self).__init__(parent)
        self.statics = None
        self.addUserView = None
        self.setupUi(self)
        self.adminID = adminID
        self.actID = actID
        self.act = [actID, act[0], act[1], act[2]]
        self.initUi()
        self.initSlot()
        self.initDT()
        self.initTable()

    def initUi(self):
        self.resize(1000, 600)
        self.setFixedSize(1000, 600)
        self.setWindowModality(Qt.ApplicationModal)
        self.name_le.setText(self.act[1])

    def initDT(self):
        self.start_dt.setDateTime(self.act[2])
        self.end_dt.setDateTime(self.act[3])
        self.end_dt.setMinimumDateTime(datetime.now())

    def initSlot(self):
        self.return_bt.clicked.connect(lambda: self.manageReturn.emit(self.act))
        self.addUser_btn.clicked.connect(self.addUserFunc)
        self.add_bt.clicked.connect(self.change)
        self.output_btn.clicked.connect(self.generateCsv)
        self.delete_btn.clicked.connect(self.delete)
        self.delete_user_btn.clicked.connect(self.deleteUser)

    def deleteUser(self):
        items = self.user_tb.selectedItems()
        db = DBUtil()
        for i in range(0, len(items), 3):
            sno = items[i].text()
            uid = db.getOne(f"select id from face.user where sno='{sno}'")[0]
            print(f"uid:{uid}")
            sql = f"delete from face.sign where user_id={int(uid)} and activity_id={self.actID}"
            db.delete(sql)
        self.initTable()

    def delete(self):
        db = DBUtil()
        db.delete(f"delete from activity where id={self.actID}")
        self.deleteSignal.emit()
        self.close()

    def change(self):
        name = self.name_le.text()
        st = self.start_dt.dateTime().toPyDateTime()
        ed = self.end_dt.dateTime().toPyDateTime()
        if name == "":
            QMessageBox.information(self, "waining", "活动名称不得为空！", QMessageBox.Ok)
            self.name_le.clear()
            self.name_le.setFocus()
            return
        if st > ed:
            QMessageBox.information(self, "waining", "开始时间不得晚于结束时间！", QMessageBox.Ok)
            return
        db = DBUtil()
        res = db.update(f"update face.activity set name='{name}', start_time='{getDateTime(st)}',"
                        f" end_time='{getDateTime(ed)}' where id={self.actID}")
        if res != 0:
            self.act = [self.actID, name, st, ed]
            self.initTable()
            self.changeSubmit.emit(self.act)
        print(f'活动{name}已修改')

    def initTable(self):
        self.user_tb.setColumnCount(3)
        self.user_tb.setHorizontalHeaderLabels(["学号", "姓名", "签到状态"])
        self.user_tb.setSelectionBehavior(1)
        self.user_tb.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_tb.setEditTriggers(QAbstractItemView.NoEditTriggers)
        datas = self.getData()
        self.user_tb.setRowCount(len(datas))
        num = len(datas)
        signed = 0
        for i in range(num):
            item0 = QTableWidgetItem(datas[i][0])
            item0.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.user_tb.setItem(i, 0, item0)
            item1 = QTableWidgetItem(datas[i][1])
            item1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.user_tb.setItem(i, 1, item1)
            item2 = QTableWidgetItem(datas[i][2])
            item2.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            if datas[i][2] == '已签到':
                signed += 1
                item2.setBackground(QBrush(QColor('green')))
            else:
                item2.setBackground(QBrush(QColor('red')))
            self.user_tb.setItem(i, 2, item2)
        absent = num - signed
        if num == 0:
            self.st_lab.setText(f"应到:0 实到:0 出勤率:0.00%")
        else:
            self.statics = [num, signed, signed/num]
            self.st_lab.setText(f"应到:{num} 实到:{signed} 出勤率:{signed / num:.2%}")
        print(num, absent)

    def getData(self):
        db = DBUtil()
        res = db.getAll(f"select u.sno, u.name, s.is_sign, s.update_time from face.user u inner join face.sign s "
                        f"on u.id=s.user_id where s.activity_id={self.actID}")
        datas = []
        for data in res:
            if data[2] == 1:
                time = data[3]
            else:
                time = ''
            datas.append([data[0], data[1], config.sign_dic[data[2]], time])
        return datas

    def generateCsv(self):
        fileName, fileType = QFileDialog.getSaveFileName(self, "保存文件", str(pathlib.Path.home())+'/签到表.csv', 'CSV (*.csv)')
        datas = self.getData()
        if fileName == "":
            return
        print(fileName)
        try:
            with open(fileName, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['学号', '姓名', '签到状态', '时间'])
                for data in datas:
                    writer.writerow([data[0], data[1], data[2], data[3]])
                writer.writerow(['实到', '应到', '出勤率'])
                writer.writerow([self.statics[0], self.statics[1], self.statics[2]])
        except Exception as e:
            print(e)
            print("导出失败！")
            return

    def addUserFunc(self):
        self.addUserView = UTA(self.adminID, self.actID)
        self.addUserView.show()
        self.addUserView.returnSuccess.connect(lambda: self.initTable())


class UTA(MyMainWindow, Ui_addUser):
    """"""
    returnSuccess = pyqtSignal()

    def __init__(self, adminID, actID, parent=None):
        super(UTA, self).__init__(parent)
        self.setupUi(self)
        self.adminID = adminID
        self.actID = actID
        self.initUi()
        self.initSlot()
        self.initTable()

    def initUi(self):
        self.setWindowModality(Qt.ApplicationModal)

    def initSlot(self):
        self.return_bt.clicked.connect(self.close)
        self.add_btn.clicked.connect(self.add)

    def add(self):
        items = self.user_tb.selectedItems()
        db = DBUtil()
        for i in range(0, len(items), 3):
            uid = items[i].text()
            print(f"uid:{uid}")
            sql = f"insert into face.sign(user_id, activity_id) values({int(uid)}, {self.actID})"
            db.save(sql)
        self.initTable()
        self.returnSuccess.emit()

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
                    where u.admin_id = {self.adminID}
                        and u.id not in (select s.user_id from face.sign s where s.activity_id = {self.actID})"""
        res = db.getAll(sql)
        return res
