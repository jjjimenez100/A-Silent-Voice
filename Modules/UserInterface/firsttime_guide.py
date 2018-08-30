from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import sys, os
from Modules.FileFinder import resource_path

# Class to show the first time guide pop up
class FirstTimeGuide(QDialog):
    def __init__(self, mainWindow):
        super().__init__()
        if getattr(sys, 'frozen', False):
            ui = resource_path('firsttime_guide.ui')
        else:
            ui = 'Modules/UserInterface/firsttime_guide.ui'
        loadUi(ui, self)
        self.step_count = 0
        self.nextButton.clicked.connect(self.nextAction)
        self.previousButton.clicked.connect(self.prevAction)
        self.mainWindow = mainWindow
        self.mainWindow.firsttime_tutorial(0)
        self.tutorial_steps.setCurrentIndex(0)

    def nextAction(self):
        if self.step_count == 0:
            self.tutorial_steps.setCurrentIndex(0)

        if self.nextButton.text() == "Done":
            self.mainWindow.firsttime_tutorial(12)
            self.closeAction()
            return
        else:
            if self.step_count < 12:
                self.step_count += 1
                self.mainWindow.firsttime_tutorial(self.step_count)
            if self.step_count >= 12:
                self.nextButton.setText('Done')
        print(self.step_count)
        self.tutorial_steps.setCurrentIndex(self.step_count)

    def prevAction(self):
        print(self.step_count)
        if self.step_count > 0:
            self.step_count -= 1
            self.mainWindow.firsttime_tutorial(self.step_count)
        if self.step_count < 12:
            self.nextButton.setText('Next')
        self.tutorial_steps.setCurrentIndex(self.step_count)

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
            print("crashed in firsttime_guide.py")

    @pyqtSlot()
    def closeAction(self):
        print("cuim")
        self.step_count += 1
        self.close()

    def closeEvent(self, evt):
        print(evt)
        if not self.step_count > 12:
            evt.ignore()
