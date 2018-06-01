from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class LogInForm(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('login_Form.ui', self)
        self.setFixedSize(623, 366)
        self.loginBtn.clicked.connect(self.openWindow) #connects login btn to the method openWindow

    @pyqtSlot()
    def openWindow(self): #for calling the main menu
        from mainController import MainForm
        self.window = MainForm(self)
        self.hide()
        self.window.show()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = LogInForm()
    window.show()
    sys.exit(app.exec_())

