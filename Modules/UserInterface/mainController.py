import cv2
import sys

from PyQt5 import Qt
from PyQt5.QtCore import QTimer, pyqtSlot, QSize, pyqtSignal, QThread
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QApplication, QPushButton, QLabel
from PyQt5.uic import loadUi
from PyQt5.uic.properties import QtGui
from Modules.UserInterface.loginController import *
import Modules.CNN.RecognizeASL as recognition
from Modules.ProcessImage import extractRegionofInterest, drawBoundingRectangle
#from OpenCVWrapper import *
#import cv2
#import Modules.UserInterface.iconpack


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    #thread = recognition.Recognition()

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            frame = drawBoundingRectangle(frame)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)
            #frame = extractRegionofInterest(frame)
            #letter = self.thread.predict(frame)
            #print(letter)


class MainForm(QMainWindow):

    def __init__(self, logWindow):
        super().__init__()
        loadUi('main_window.ui', self)
        #self.camera = cv2.VideoCapture(0)

        self.stackedWidget.setCurrentIndex(3)
        self.logoutButton.clicked.connect(self.logoutAction)
        self.homeButton.clicked.connect(self.showHomePage)
        self.settingsButton.clicked.connect(self.showSettingsPage)
        self.helpButton.clicked.connect(self.showHelp)
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

    def showHelp(self):
        self.stackedWidget.setCurrentIndex(2)

    def showAbout(self):
        self.stackedWidget.setCurrentIndex(3)

    @pyqtSlot()
    def logoutAction(self):
        self.close()
        self.loginWindow.show()
        self.loginWindow.passText.clear()
        self.loginWindow.userText.clear()
