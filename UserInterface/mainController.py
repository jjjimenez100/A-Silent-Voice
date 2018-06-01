from loginController import *

class MainForm(QMainWindow):
    def __init__(self, logWindow):
        super().__init__()
        loadUi('main_window.ui', self)
        self.logoutBtn.clicked.connect(self.logoutAction)
        self.loginWindow = logWindow
    @pyqtSlot()
    def logoutAction(self):
        self.close()
        self.loginWindow.show()
        self.loginWindow.passText.clear()
        self.loginWindow.userText.clear()

