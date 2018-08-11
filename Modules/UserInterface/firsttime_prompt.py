from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

class FirstTimePrompt(QDialog):
    def __init__(self, mainWindow):
        super().__init__()
        loadUi('firsttime_prompt.ui', self)
        self.okayButton.clicked.connect(self.closeAction)
        self.mainWindow = mainWindow

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)

    @pyqtSlot()
    def closeAction(self):
        self.close()