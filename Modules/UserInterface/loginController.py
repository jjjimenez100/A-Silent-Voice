import random, time

from PyQt5.QtCore import pyqtSlot, QByteArray, QTimer, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import os
#os.environ["CUDA_VISIBLE_DEVICES"]="-1"
from PyQt5.QtCore import QThread, pyqtSignal
import PyQt5.QtGui as gui
from PyQt5.uic.properties import QtCore
from Modules.CNN.TFModel import TFModel
from Modules.UserInterface.mainController import MainForm
import cv2

class Loading(QThread):

    progress = pyqtSignal("PyQt_PyObject", int)

    def __init__(self):
        super(Loading, self).__init__()

    def run(self):
        print("starting", flush=True)
        model = TFModel("output_graph.pb", "output_labels.txt", "Placeholder", "final_result")

        count = 0
        available = []
        while True:
            test = cv2.VideoCapture(count)
            if test is None or not test.isOpened():
                break
            available.append(count)
            count += 1

        self.progress.emit(model, len(available))


class LogInForm(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('login_Form.ui', self)
        self.setFixedSize(340, 450)
        movie = QMovie("loading.gif")
        self.logoIMG.setMovie(movie)
        movie.start()
        self.loadMainForm()

        print("loading main form")

        #self.button_skip.clicked.connect(self.openMainForm)
        self.task = Loading()
        self.task.progress.connect(self.setMainForm)
        self.task.finished.connect(self.openMainForm)
        self.task.start()
        #self.button_skip.clicked.connect(self.loadMainForm)
        print("show loading")
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.show()

    def loadMainForm(self): #for calling the main menu
        pass

    @pyqtSlot("PyQt_PyObject", int)
    def setMainForm(self, model, cameraCount):
        self.model = model
        self.cameraCount = cameraCount

    def openMainForm(self):
        self.task.wait()
        self.task.quit()
        self.task = None
        self.window = MainForm(self, self.model, self.cameraCount)
        self.window.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.window.show()
        self.close()


if __name__ == '__main__':
    import sys

    sys._excepthook = sys.excepthook


    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    window = LogInForm()
    sys.exit(app.exec_())# program still runs even if you quit on login window