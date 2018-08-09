import random, time

from PyQt5.QtCore import pyqtSlot, QByteArray, QTimer, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
import iconpack
from PyQt5.QtCore import QThread, pyqtSignal
import PyQt5.QtGui as gui
from PyQt5.uic.properties import QtCore
from Modules.CNN.TFModel import TFModel
from Modules.UserInterface.mainController import MainForm

class Loading(QThread):

    progress = pyqtSignal("PyQt_PyObject")

    def __init__(self):
        super(Loading, self).__init__()

    def run(self):
        print("starting", flush=True)
        model = TFModel("output_graph.pb", "output_labels.txt", "Placeholder", "final_result")
        self.progress.emit(model)


class LogInForm(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('login_Form.ui', self)
        self.setFixedSize(340, 450)
        movie = QMovie("loading.gif")
        self.logoIMG.setMovie(movie)
        movie.start()
        self.loadMainForm()

        #self.button_skip.clicked.connect(self.openMainForm)
        self.task = Loading()
        self.task.progress.connect(self.setMainForm)
        self.task.finished.connect(self.openMainForm)
        self.task.start()
        #self.button_skip.clicked.connect(self.loadMainForm)

    def loadMainForm(self): #for calling the main menu
        pass

    @pyqtSlot("PyQt_PyObject")
    def setMainForm(self, model):
        self.model = model

    def openMainForm(self):
        self.window = MainForm(self, self.model)
        self.window.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.window.show()
        self.hide()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = LogInForm()
    window.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
    window.show()
    sys.exit(app.exec_())# program still runs even if you quit on login window