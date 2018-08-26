from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys, os
#os.environ["CUDA_VISIBLE_DEVICES"]="-1"
from PyQt5.QtCore import QThread, pyqtSignal
from Modules.CNN.TFModel import TFModel
from Modules.UserInterface.mainController import MainForm
from cv2 import VideoCapture
import Modules.RecognitionThread as rt
from Modules.FileFinder import resource_path


# Loading class to load modules needed for the main thread
class Loading(QThread):
    progress = pyqtSignal("PyQt_PyObject", int)

    def __init__(self, label):
        super(Loading, self).__init__()
        # self.label_load = label

    def run(self):
        print("starting", flush=True)
        print("bueno")
        model = TFModel(resource_path("output_graph.pb"), resource_path("output_labels.txt"), "Placeholder",
                        "final_result")
        print("model loaded")
        # self.label_load.setText("Loading: Model")
        count = 0
        available = []
        while True:
            test = VideoCapture(count)
            if test is None or not test.isOpened():
                break
            available.append(count)
            count += 1
        print(count)
        if count > 0:
            vid = VideoCapture(0)
            _, frame = vid.read()

            load = rt.Recoginize(model)
            load.daemon = True
            load.start()
            load.predict(frame)
            from time import sleep
            sleep(1)
            load.predict("kill")
            load.join()
            vid.release()
            print("model loaded")
            # self.label_load.setText("Loaded Model")
        print("donezo")
        # self.label_load.setText("Finalizing")
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
        self.update_loading("Loading: Graphical User Interface")
        print("loading main form")
        self.task = Loading(self.labelLoad)
        self.task.progress.connect(self.setMainForm)
        self.task.finished.connect(self.openMainForm)
        self.task.start()
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.show()

    # Updates the loading message
    def update_loading(self, message):
        self.labelLoad.setText(message)

    # Signal receiver to get loaded data
    @pyqtSlot("PyQt_PyObject", int)
    def setMainForm(self, model, count):
        self.model = model
        self.available = count

    # Starts the main form and finishes the loading sequence
    def openMainForm(self):
        self.update_loading('Opening Main form')
        self.task.wait()
        self.task.quit()

        self.window = MainForm(self.model, self.available)
        self.window.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.window.show()
        self.close()
        self.window.openFirstTimeDialog()
