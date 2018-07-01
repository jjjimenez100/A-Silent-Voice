import sys

from PyQt5.QtCore import QTimer, pyqtSlot, QSize
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QApplication, QPushButton, QLabel
from PyQt5.uic import loadUi
from PyQt5.uic.properties import QtGui
from loginController import *
from OpenCVWrapper import *
import cv2
import iconpack

class MainForm(QMainWindow):

    def __init__(self, logWindow):
        super().__init__()
        loadUi('main_window.ui', self)
        #self.camera = cv2.VideoCapture(0)

        self.stackedWidget.setCurrentIndex(0)
        self.logoutButton.clicked.connect(self.logoutAction)
        self.homeButton.clicked.connect(self.showHomePage)
        self.contactsButton.clicked.connect(self.showContactsPage)
        self.settingsButton.clicked.connect(self.showSettingsPage)
        self.aboutButton.clicked.connect(self.showAbout)

        self.loginWindow = logWindow

    def showHomePage(self):
        self.stackedWidget.setCurrentIndex(0)

    def showContactsPage(self):
        self.stackedWidget.setCurrentIndex(3)

    def showSettingsPage(self):
        self.stackedWidget.setCurrentIndex(1)

    def showAbout(self):
        self.stackedWidget.setCurrentIndex(2)

    @pyqtSlot()
    def logoutAction(self):
        self.close()
        self.loginWindow.show()
        self.loginWindow.passText.clear()
        self.loginWindow.userText.clear()
