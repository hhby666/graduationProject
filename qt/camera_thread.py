# -*- coding: utf-8 -*-

"""
Author:by wlq on 2023/4/22 20:53
FileName:camera_thread.py in GraduationProject
Tools:PyCharm python3.9
"""
import time

import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage


class Camera(QThread):
    """"""
    cameraSignal = pyqtSignal(object)
    faceSignal = pyqtSignal(object)

    def __init__(self, dev=0, parent=None):
        super(Camera, self).__init__(parent)
        self.cap = cv2.VideoCapture()
        self.dev = dev

    def run(self):
        isOpen = self.cap.open(self.dev)
        print(f"摄像头线程已启动 {isOpen}")
        num = 20
        while isOpen:
            flag, frame = self.cap.read()
            rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            show = cv2.resize(rgb_img, (640, 480))
            pix = QPixmap.fromImage(QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888))
            self.cameraSignal.emit(pix)
            if num >= 0:
                num -= 1
            else:
                self.faceSignal.emit(show)
                print(time.time())
                num = 20
            time.sleep(0.03)
