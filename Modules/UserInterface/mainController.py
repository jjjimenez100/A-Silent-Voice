import cv2
import sys

from PyQt5 import Qt
from PyQt5.QtCore import QTimer, pyqtSlot, QSize, pyqtSignal, QThread
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QApplication, QPushButton, QLabel
from PyQt5.uic import loadUi
from PyQt5.uic.properties import QtGui
from loginController import *
#from OpenCVWrapper import *
#import cv2
import iconpack


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)


class MainForm(QMainWindow):

    def __init__(self, logWindow):
        super().__init__()
        loadUi('main_window.ui', self)
        #self.camera = cv2.VideoCapture(0)

        self.stackedWidget.setCurrentIndex(0)
        self.logoutButton.clicked.connect(self.logoutAction)
        self.homeButton.clicked.connect(self.showHomePage)
        self.settingsButton.clicked.connect(self.showSettingsPage)
        self.aboutButton.clicked.connect(self.showAbout)
        self.quitButton.clicked.connect(self.logoutAction)
        self.hideButton.clicked.connect(self.showMinimized)
        self.minmaxButton.clicked.connect(self.minmaxWindow)
        print(self.videoLabel.width())
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        self.loginWindow = logWindow

    def minmaxWindow(self):
        if self.minmaxButton.isChecked():
            self.showMaximized()
        else:
            self.showNormal()



    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))

    def showHomePage(self):
        self.stackedWidget.setCurrentIndex(0)

    def showSettingsPage(self):
        self.stackedWidget.setCurrentIndex(1)

    def showAbout(self):
        self.stackedWidget.setCurrentIndex(2)

    @pyqtSlot()
    def logoutAction(self):
        self.close()
