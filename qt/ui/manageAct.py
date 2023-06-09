# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'manageAct.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_manageAct(object):
    def setupUi(self, manageAct):
        manageAct.setObjectName("manageAct")
        manageAct.resize(992, 600)
        manageAct.setStyleSheet("* {\n"
"    background-color: white;\n"
"    font: 12pt \"YaHei Monaco Hybird\";\n"
"}\n"
"QPushButton{\n"
"    background-color: skyblue;\n"
"}\n"
"QLabel{\n"
"    font: 12pt \"YaHei Monaco Hybird\";\n"
"}")
        self.centralwidget = QtWidgets.QWidget(manageAct)
        self.centralwidget.setObjectName("centralwidget")
        self.end_dt = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.end_dt.setGeometry(QtCore.QRect(150, 210, 241, 31))
        self.end_dt.setObjectName("end_dt")
        self.name_lab_3 = QtWidgets.QLabel(self.centralwidget)
        self.name_lab_3.setGeometry(QtCore.QRect(40, 210, 101, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(60)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.name_lab_3.sizePolicy().hasHeightForWidth())
        self.name_lab_3.setSizePolicy(sizePolicy)
        self.name_lab_3.setTextFormat(QtCore.Qt.PlainText)
        self.name_lab_3.setObjectName("name_lab_3")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(29, 90, 371, 33))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.name_lab = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(60)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.name_lab.sizePolicy().hasHeightForWidth())
        self.name_lab.setSizePolicy(sizePolicy)
        self.name_lab.setTextFormat(QtCore.Qt.PlainText)
        self.name_lab.setObjectName("name_lab")
        self.horizontalLayout.addWidget(self.name_lab)
        self.name_le = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.name_le.sizePolicy().hasHeightForWidth())
        self.name_le.setSizePolicy(sizePolicy)
        self.name_le.setBaseSize(QtCore.QSize(220, 30))
        self.name_le.setText("")
        self.name_le.setObjectName("name_le")
        self.horizontalLayout.addWidget(self.name_le)
        self.start_dt = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.start_dt.setGeometry(QtCore.QRect(150, 150, 241, 31))
        self.start_dt.setObjectName("start_dt")
        self.name_lab_2 = QtWidgets.QLabel(self.centralwidget)
        self.name_lab_2.setGeometry(QtCore.QRect(40, 150, 101, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(60)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.name_lab_2.sizePolicy().hasHeightForWidth())
        self.name_lab_2.setSizePolicy(sizePolicy)
        self.name_lab_2.setTextFormat(QtCore.Qt.PlainText)
        self.name_lab_2.setObjectName("name_lab_2")
        self.layoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(60, 280, 300, 36))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.add_bt = QtWidgets.QPushButton(self.layoutWidget_2)
        self.add_bt.setObjectName("add_bt")
        self.horizontalLayout_6.addWidget(self.add_bt)
        self.return_bt = QtWidgets.QPushButton(self.layoutWidget_2)
        self.return_bt.setObjectName("return_bt")
        self.horizontalLayout_6.addWidget(self.return_bt)
        self.user_tb = QtWidgets.QTableWidget(self.centralwidget)
        self.user_tb.setGeometry(QtCore.QRect(440, 20, 541, 501))
        self.user_tb.setObjectName("user_tb")
        self.user_tb.setColumnCount(0)
        self.user_tb.setRowCount(0)
        self.output_btn = QtWidgets.QPushButton(self.centralwidget)
        self.output_btn.setGeometry(QtCore.QRect(450, 530, 151, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(150)
        sizePolicy.setVerticalStretch(40)
        sizePolicy.setHeightForWidth(self.output_btn.sizePolicy().hasHeightForWidth())
        self.output_btn.setSizePolicy(sizePolicy)
        self.output_btn.setObjectName("output_btn")
        self.addUser_btn = QtWidgets.QPushButton(self.centralwidget)
        self.addUser_btn.setGeometry(QtCore.QRect(830, 530, 151, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(150)
        sizePolicy.setVerticalStretch(40)
        sizePolicy.setHeightForWidth(self.addUser_btn.sizePolicy().hasHeightForWidth())
        self.addUser_btn.setSizePolicy(sizePolicy)
        self.addUser_btn.setObjectName("addUser_btn")
        self.delete_btn = QtWidgets.QPushButton(self.centralwidget)
        self.delete_btn.setGeometry(QtCore.QRect(60, 340, 301, 34))
        self.delete_btn.setObjectName("delete_btn")
        self.st_lab = QtWidgets.QLabel(self.centralwidget)
        self.st_lab.setGeometry(QtCore.QRect(60, 450, 311, 31))
        self.st_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.st_lab.setObjectName("st_lab")
        self.delete_user_btn = QtWidgets.QPushButton(self.centralwidget)
        self.delete_user_btn.setGeometry(QtCore.QRect(640, 530, 151, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(150)
        sizePolicy.setVerticalStretch(40)
        sizePolicy.setHeightForWidth(self.delete_user_btn.sizePolicy().hasHeightForWidth())
        self.delete_user_btn.setSizePolicy(sizePolicy)
        self.delete_user_btn.setObjectName("delete_user_btn")
        manageAct.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(manageAct)
        self.statusbar.setObjectName("statusbar")
        manageAct.setStatusBar(self.statusbar)

        self.retranslateUi(manageAct)
        QtCore.QMetaObject.connectSlotsByName(manageAct)

    def retranslateUi(self, manageAct):
        _translate = QtCore.QCoreApplication.translate
        manageAct.setWindowTitle(_translate("manageAct", "管理活动"))
        self.name_lab_3.setText(_translate("manageAct", "结束时间:"))
        self.name_lab.setText(_translate("manageAct", "当前活动:"))
        self.name_le.setPlaceholderText(_translate("manageAct", "请输入活动名"))
        self.name_lab_2.setText(_translate("manageAct", "开始时间:"))
        self.add_bt.setText(_translate("manageAct", "提交"))
        self.return_bt.setText(_translate("manageAct", "返回"))
        self.output_btn.setText(_translate("manageAct", "导出签到表"))
        self.addUser_btn.setText(_translate("manageAct", "添加签到人员"))
        self.delete_btn.setText(_translate("manageAct", "删除此活动"))
        self.st_lab.setText(_translate("manageAct", "TextLabel"))
        self.delete_user_btn.setText(_translate("manageAct", "删除选中人员"))
