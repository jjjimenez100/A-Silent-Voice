import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.uic.properties import QtGui
from PyQt5.uic import loadUi

class QuitPrompt(QDialog):
    def __init__(self, mainWindow):
        super().__init__()
        loadUi('quit_prompt.ui', self)
        self.quitYesButton.clicked.connect(self.logoutAction)
        self.quitNoButton.clicked.connect(self.closePrompt)
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
    def logoutAction(self):
        self.close()
        #self.mainWindow.Q
        sys.exit(QtGui.QApplication(sys.argv).exec_())
        #self.loginWindow.show()

    @pyqtSlot()
    def closePrompt(self):
        self.close()
        # self.loginWindow.show()


