# -*- coding: utf-8 -*-

"""
Author:by wlq on 2023/4/22 21:37
FileName:mainThread.py in GraduationProject
Tools:PyCharm python3.9
"""
import os
import time
from datetime import datetime

import cv2
import face_recognition
import numpy
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *

from qt.call_addAct import AddAct
from qt.call_addUser import AddUser
from qt.call_login import Login
from qt.call_manageAct import ManageAct
from qt.call_manageUser import ManageUser
from qt.camera_thread import Camera
from qt.module import MyMainWindow
from qt.ui.mainUI import Ui_MainWindow
from tool import config
from tool.DBUtil import DBUtil
from tool.EmailUtil import EmailUtil
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage


class FaceRecognition(QThread):
    """"""
    resultSignal = pyqtSignal(object)

    def __init__(self, face, features, datas, parent=None):
        super(FaceRecognition, self).__init__(parent)
        self.face = face
        self.features = features
        self.datas = datas

    def run(self):
        encodings = face_recognition.face_encodings(self.face)
        if len(encodings) == 0:
            return None
        res = face_recognition.compare_faces(self.features, encodings[0], tolerance=0.4)
        idx = -1
        try:
            idx = res.index(True)
        except Exception as e:
            print(f"error: {e} 无匹配人脸信息")
            self.resultSignal.emit(None)
        if idx == -1:
            msg = None
        else:
            msg = self.datas[idx]
        self.resultSignal.emit(msg)


class MainWindow(MyMainWindow, Ui_MainWindow):
    """"""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.timer = QTimer()
        self.login = Login()
        self.addUser = AddUser()
        self.addAct = AddAct()
        self.cameraThread = Camera()
        self.acts = {}
        self.manageAct = None
        self.manageUser = None
        self.actID = None
        self.image = None
        self.adminID = None
        self.faceThread = None
        self.setupUi(self)
        self.initUi()
        self.initSlot()

    def initUi(self):
        """初始化UI"""
        # 先进行登录
        self.login.show()

        # 设置大小
        self.resize(1000, 600)
        self.setFixedSize(1000, 600)

        # 未打开摄像头时禁用检测和录入功能
        self.start_btn.setDisabled(True)
        self.add_user_btn.setDisabled(True)

    def initAct(self):
        """初始化活动选择下拉框"""
        self.act_cb.clear()
        db = DBUtil()
        acts = db.getAll(f"select id,name,start_time,end_time from face.activity where admin_id={self.adminID}")
        if len(acts) == 0:
            # 如果当前管理员无活动先提示添加活动
            QMessageBox.information(self, "waining", "暂无活动请先创建活动", QMessageBox.Ok)
            self.addAct.adminID = self.adminID
            self.addAct.show()
        else:
            for act in acts:
                self.acts[act[0]] = [act[1], act[2], act[3]]
                self.act_cb.addItem(f"{act[0]}:{self.acts[act[0]][0]}")

    def initSlot(self):
        """连接信号和槽"""
        self.login.successLogin.connect(self.loginSuccess)
        self.addUser.addReturn.connect(self.addUserSuccess)
        self.addAct.addReturn.connect(self.addActSuccess)
        self.cameraThread.cameraSignal.connect(self.showImage)
        self.cameraThread.faceSignal.connect(self.getImage)
        self.timer.timeout.connect(self.showResult)

        self.open_btn.clicked.connect(self.openCamera)
        self.quit_btn.clicked.connect(self.close)
        self.add_user_btn.clicked.connect(self.addUserFunc)
        self.act_cb.currentTextChanged.connect(self.changeAct)
        self.add_act_btn.clicked.connect(self.addActFunc)
        self.manage_btn.clicked.connect(self.manageActFunc)
        self.start_btn.clicked.connect(self.startFunc)
        self.manage_msg_btn.clicked.connect(self.manageUserFunc)

    def loginSuccess(self, admin_id):
        """登录成功后执行"""
        self.adminID = admin_id
        self.initAct()
        self.show()
        self.login.destroy()

    def openCamera(self):
        """打开摄像头"""
        if self.cameraThread.isRunning():
            self.cameraThread.terminate()
            self.closeCamera()
            self.start_btn.setDisabled(True)
            self.add_user_btn.setDisabled(True)
        else:
            self.cameraThread.start()
            self.open_btn.setText("关闭摄像头")
            self.open_btn.setStyleSheet("background-color: blue;")
            self.start_btn.setDisabled(False)
            self.add_user_btn.setDisabled(False)

    def closeCamera(self):
        """关闭摄像头"""
        self.open_btn.setText("打开摄像头")
        self.open_btn.setStyleSheet("background-color: skyblue;")
        self.initLabel()

    def showImage(self, pix):
        """将图片展示到 QLabel 上"""
        self.camera_lab.setPixmap(pix)

    def getImage(self, image):
        self.image = image

    def addUserFunc(self):
        """录入人脸功能"""
        try:
            if self.getFace():
                self.addUser.adminID = self.adminID
                self.addUser.show()
            else:
                print("error!")
                return
        except Exception as e:
            print(e)

    def getFace(self):
        """获取摄像头拍摄的人脸并标记人脸位置显示到QLabel上"""
        locs = face_recognition.face_locations(self.image)
        if len(locs) == 0:
            return False
        top, right, bottom, left = locs[0]
        self.addUser.feature = face_recognition.face_encodings(self.image)[0]
        cv2.rectangle(self.image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.resize(self.image, (640, 480))
        self.addUser.face_lab.setPixmap(
            QPixmap.fromImage(QImage(self.image.data, self.image.shape[1], self.image.shape[0], QImage.Format_RGB888)))
        return True

    def initLabel(self):
        self.camera_lab.setText("摄像头")
        self.camera_lab.setStyleSheet("border:5px solid rgb(255,170,0);")

    def closeEvent(self, event):
        """重写关闭事件"""
        ok = QPushButton()
        cancel = QPushButton()
        msg = QMessageBox(QMessageBox.Warning, '关闭', '是否关闭！')
        msg.addButton(ok, QMessageBox.ActionRole)
        msg.addButton(cancel, QMessageBox.RejectRole)
        ok.setText('确定')
        cancel.setText('取消')
        if msg.exec_() == QMessageBox.RejectRole:
            event.ignore()
        else:
            if self.cameraThread.isRunning():
                self.cameraThread.terminate()
            event.accept()
            os._exit(0)

    def addUserSuccess(self):
        """添加用户成功后执行"""
        self.addUser.feature = None
        self.addUser.close()
        self.addUser.destroy()

    def changeAct(self, name):
        """活动更改后执行"""
        if name == '':
            return
        else:
            print(f"当前活动:{name}")
            self.actID = int(name.split(":")[0])

    def addActSuccess(self):
        """添加活动成功后执行"""
        self.addAct.close()
        self.addAct.destroy()
        self.initAct()

    def addActFunc(self):
        """添加活动功能"""
        self.addAct.adminID = self.adminID
        self.addAct.show()

    def manageActFunc(self):
        """管理活动功能"""
        print(self.adminID, self.actID, self.acts[self.actID])
        self.manageAct = ManageAct(self.adminID, self.actID, self.acts[self.actID])
        self.manageAct.manageReturn.connect(self.manageActSuccess)
        self.manageAct.changeSubmit.connect(self.updateAct)
        self.manageAct.deleteSignal.connect(self.initAct)
        self.manageAct.show()

    def manageActSuccess(self, act):
        """结束管理活动后执行"""
        self.manageAct.close()
        self.manageAct.destroy()
        self.updateAct(act)

    def updateAct(self, act):
        """活动更新后执行"""
        self.act_cb.setItemText(self.act_cb.currentIndex(), f"{act[0]}:{act[1]}")
        self.actID = act[0]
        self.acts[self.actID] = [act[1], act[2], act[3]]

    def manageUserFunc(self):
        self.manageUser = ManageUser(self.adminID)
        self.manageUser.show()

    def showResult(self):
        """展示识别结果"""
        # datas, features = self.getData()
        # self.faceThread = FaceRecognition(self.image, features, datas)
        # self.faceThread.resultSignal.connect(self.displayMsg)
        # self.faceThread.start()

        msg = self.recognition()
        if msg is not None:
            self.result_lab.setText(f"id: {msg['id']}, sno:{msg['sno']}, name:{msg['name']}")
            self.result_lab.setStyleSheet("background-color: green")
            self.sign(msg)
        else:
            self.result_lab.clear()
            self.result_lab.setStyleSheet("background-color: white")
            return

    def displayMsg(self, msg):
        if msg is not None:
            self.result_lab.setText(f"id: {msg['id']}, sno:{msg['sno']}, name:{msg['name']}")
            self.result_lab.setStyleSheet("background-color: green")
            self.sign(msg)
        else:
            self.result_lab.clear()
            self.result_lab.setStyleSheet("background-color: white")

    def startFunc(self):
        """开始检测"""
        if self.timer.isActive():
            self.timer.stop()
            self.start_btn.setText("开始检测")
            self.start_btn.setStyleSheet("background-color: skyblue;")
            self.result_lab.clear()
            self.open_btn.setDisabled(False)
            self.act_cb.setDisabled(False)
            self.result_lab.setStyleSheet("background-color: white")
        else:
            self.timer.start(1000)
            self.start_btn.setStyleSheet("background-color: blue;")
            self.start_btn.setText("停止检测")
            self.open_btn.setDisabled(True)
            self.act_cb.setDisabled(True)

    def recognition(self):
        """人脸识别"""
        datas, features = self.getData()
        rgb_img = self.image
        encodings = face_recognition.face_encodings(rgb_img)
        if len(encodings) == 0:
            return None
        res = face_recognition.compare_faces(features, encodings[0], tolerance=0.4)
        try:
            idx = res.index(True)
        except Exception as e:
            print(f"error: {e} 无匹配人脸信息")
            return None
        print(datas[idx])
        return datas[idx]

    def getData(self):
        """获取参加活动签到人员的数据"""
        db = DBUtil()
        sql = f"select u.id, u.sno, u.name, u.feature, u.email, s.is_sign from face.user u " \
              f"inner join face.sign s on u.id = s.user_id where s.activity_id={self.actID}"  # and s.is_sign=0"
        res = db.getAll(sql)
        datas = []
        features = []
        for data in res:
            feature = str2feature(data[3])
            dic = {
                'id': data[0],
                'sno': data[1],
                'name': data[2],
                'email': data[4],
                'is_sign': config.sign_dic[data[5]]
            }
            datas.append(dic)
            features.append(feature)
        return datas, features

    def sign(self, data):
        """识别后签到并发送邮件通知"""
        if data['is_sign'] != '未签到':
            return
        st = self.acts[self.actID][1]
        ed = self.acts[self.actID][2]
        nt = datetime.now()
        email = EmailUtil()
        db = DBUtil()
        if nt > st:
            if nt > ed:
                sql = f"update face.sign set is_sign=2 where user_id={data['id']} and activity_id = {self.actID}"
                db.update(sql)
                content = {
                    'subject': "签到通知",
                    'body': f"{data['name']},您参加的{self.acts[self.actID][0]}活动已经迟到！"
                }
                email.sendOne(data['email'], content)
            else:
                sql = f"update face.sign set is_sign=1 where user_id={data['id']} and activity_id = {self.actID}"
                db.update(sql)
                content = {
                    'subject': "签到通知",
                    'body': f"{data['name']},您参加的{self.acts[self.actID][0]}活动已经成功签到！"
                }
                email.sendOne(data['email'], content)


def str2feature(encoding_str):
    """将字符串转换为numpy数组"""
    dlist = encoding_str.strip(' ').split(',')
    dFloat = list(map(float, dlist))
    face_encoding = numpy.array(dFloat)
    return face_encoding
