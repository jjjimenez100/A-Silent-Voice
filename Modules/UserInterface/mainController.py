
from PyQt5.QtGui import QImage, QPixmap, QIcon
import PyQt5.QtGui as gui
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot, Qt
import cv2
from Modules.ProcessImage import drawBoundingRectangle, extractRegionofInterest
import Modules.RecognitionThread as rt
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *

class Thread(QThread):
    changePixmap = pyqtSignal(QImage, str)
    def __init__(self, model):
        super(Thread, self).__init__()
        self.thread = rt.Recoginize(model)
        self.thread.start()

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            frame = drawBoundingRectangle(frame)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            frame = extractRegionofInterest(frame)
            self.thread.predict(frame)
            letter, acc = self.thread.getPrediction()
            print('letter:',letter)
            self.changePixmap.emit(p, letter)

class MainForm(QMainWindow):

    def __init__(self, logWindow, model):
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
        self.thread = Thread(model)
        self.thread.changePixmap.connect(self.setImage)
        self.loginWindow = logWindow

    #def setFormWords(self):


    def event(self, ev):
        if type(ev) == gui.QShowEvent:
            self.thread.start()
        return super(MainForm, self).event(ev)

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

    @pyqtSlot(QImage, str)
    def setImage(self, image, letter):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))
        self.letterLabel.setText("Recognized Letter: "+letter)

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
