# importing required libraries
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import os
import sys
import time
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.Window | Qt.WindowStaysOnTopHint)
        self.setGeometry(1300, 700, 160*2, 90*2)
        self.available_cameras = QCameraInfo.availableCameras()
        if not self.available_cameras:
            sys.exit()
        self.viewfinder = QCameraViewfinder()
        self.viewfinder.show()
        self.setCentralWidget(self.viewfinder)
        self.select_camera(0)
        self.setWindowTitle("Capture tự chế")
        self.show()
    def select_camera(self, i):
        self.camera = QCamera(self.available_cameras[i])
        self.camera.setViewfinder(self.viewfinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))
        self.camera.start()
        self.capture = QCameraImageCapture(self.camera)
        self.capture.error.connect(lambda error_msg, error,msg: self.alert(msg))
        self.capture.imageCaptured.connect(lambda d, 
                                i: self.status.showMessage("Image captured : " 
                                + str(self.save_seq)))
        self.current_camera_name = self.available_cameras[i].description()
        self.save_seq = 0
    def alert(self, msg):
        error = QErrorMessage(self)
        error.showMessage(msg)
if __name__ == "__main__" :
    App = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(App.exec())