import sys, os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.uic.properties import QtGui
from PyQt5.uic import loadUi

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class QuitPrompt(QDialog):
    def __init__(self, mainWindow):
        super().__init__()
        if getattr(sys, 'frozen', False):
            ui = resource_path('quit_prompt.ui')
        else:
            ui = 'Modules/UserInterface/quit_prompt.ui'
        loadUi(ui, self)
        self.quitYesButton.clicked.connect(self.logoutAction)
        self.quitNoButton.clicked.connect(self.closePrompt)
        self.mainWindow = mainWindow
        self.ans = True

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
            print("crash in quitcontroller.py")

    def getButtonPressed(self):
        print(self.ans)
        return self.ans

    @pyqtSlot()
    def logoutAction(self):
        self.ans = True
        self.hide()
        # self.close()
        # #self.mainWindow.Q
        # sys.exit(QtGui.QApplication(sys.argv).exec_())
        #self.loginWindow.show()

    @pyqtSlot()
    def closePrompt(self):
        self.ans = False
        self.hide()
        # self.close()
        # self.loginWindow.show()


