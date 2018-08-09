import random, time

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from os import path
import sys
#os.environ["CUDA_VISIBLE_DEVICES"]="-1"
from PyQt5.QtCore import QThread, pyqtSignal
from Modules.CNN.TFModel import TFModel
from Modules.UserInterface.mainController import MainForm
from cv2 import VideoCapture
from queue import Queue
import Modules.RecognitionThread as rt

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)

class Loading(QThread):

    progress = pyqtSignal("PyQt_PyObject", int)

    def __init__(self):
        super(Loading, self).__init__()

    def run(self):
        print("starting", flush=True)
        model = TFModel(resource_path("output_graph.pb"), resource_path("output_labels.txt"), "Placeholder", "final_result")

        count = 0
        available = []
        while True:
            test = VideoCapture(count)
            if test is None or not test.isOpened():
                break
            available.append(count)
            count += 1
        vid = VideoCapture(0)
        _, frame = vid.read()

        que = Queue()
        load = rt.Recoginize(model, que)
        que.put(frame)
        load.daemon = False
        load.start()
        load.predict("kill")
        load.join()

        vid.release()


        self.progress.emit(model, len(available))


class LogInForm(QDialog):
    def __init__(self):
        print("start splash")
        super().__init__()
        if getattr(sys, 'frozen', False):
            ui = 'login_Form.ui'
            loadUi(resource_path(ui), self)
            movie = QMovie(resource_path("loading.gif"))
        else:
            ui = 'Modules/UserInterface/login_Form.ui'
            loadUi(ui, self)
            movie = QMovie("Modules/UserInterface/loading.gif")
        self.setFixedSize(340, 450)
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
        
        self.window = MainForm(self.model, self.cameraCount)
        self.window.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.window.show()
        self.close()
