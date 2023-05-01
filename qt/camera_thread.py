# -*- coding: utf-8 -*-

"""
Author:by wlq on 2023/4/22 20:53
FileName:camera_thread.py in GraduationProject
Tools:PyCharm python3.9
"""
import time

import cv2
from PyQt5.QtCore import QThread, pyqtSignal


class Camera(QThread):
    """"""
    cameraSignal = pyqtSignal(object)

    def __init__(self, dev=0, parent=None):
        super(Camera, self).__init__(parent)
        self.cap = cv2.VideoCapture()
        self.dev = dev

    def run(self):
        isOpen = self.cap.open(self.dev)
        print(f"摄像头线程已启动 {isOpen}")
        while isOpen:
            flag, frame = self.cap.read()
            rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            show = cv2.resize(rgb_img, (640, 480))
            self.cameraSignal.emit(show)
            time.sleep(0.03)
