import sys, os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.uic.properties import QtGui
from PyQt5.uic import loadUi
from Modules.FileFinder import resource_path

# Class to show the quit prompt when exiting the program
class WebcamPrompt(QDialog):
    def __init__(self, mainWindow):
        super().__init__()
        if getattr(sys, 'frozen', False):
            ui = resource_path('webcam_disconnected.ui')
        else:
            ui = 'Modules/UserInterface/webcam_disconnected.ui'
        loadUi(ui, self)
        self.okButton.clicked.connect(self.closePrompt)
        self.mainWindow = mainWindow
        self.ans = False

    def change_label(self, text):
        self.label.setText(text)

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
        except:
            print("crash in", __name__)

    def getButtonPressed(self):
        print(self.ans)
        return self.ans

    @pyqtSlot()
    def logoutAction(self):
        self.ans = True
        self.hide()

    @pyqtSlot()
    def closePrompt(self):
        self.ans = False
        self.hide()
