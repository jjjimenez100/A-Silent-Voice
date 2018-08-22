from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import sys, os
from Modules.FileFinder import resource_path

# Class to show the first time guide prompt
class FirstTimePrompt(QDialog):
    def __init__(self, mainWindow):
        super().__init__()
        if getattr(sys, 'frozen', False):
            ui = resource_path('firsttime_prompt.ui')
        else:
            ui = 'Modules/UserInterface/firsttime_prompt.ui'
        loadUi(ui, self)
        self.noButton.clicked.connect(self.closeAction)
        self.yesButton.clicked.connect(self.start_tutorial)
        self.mainWindow = mainWindow

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def start_tutorial(self):
        self.closeAction()
        self.mainWindow.startTutorial()

    def mouseMoveEvent(self, event):
        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
        except:
            print('crash in firstime_prompt.py')

    @pyqtSlot()
    def closeAction(self):
        self.close()
