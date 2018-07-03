import random

from PyQt5.QtCore import pyqtSlot, QByteArray
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import iconpack


class LogInForm(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('login_Form.ui', self)
        self.setFixedSize(877, 625)
        self.loginBtn.clicked.connect(self.openMainForm) #connects login btn to the method openWindow

    @pyqtSlot()
    def openMainForm(self): #for calling the main menu
        from mainController import MainForm

        self.progressBar.setMinimumHeight(40)
        self.completed = 0
        while self.completed < 100:
            self.completed += random.uniform(0.0001, 0.00006)
            self.progressBar.setValue(self.completed)

        self.window = MainForm(self)
        self.hide()
        self.window.show()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = LogInForm()
    window.show()
    sys.exit(app.exec_())# program still runs even if you quit on login window