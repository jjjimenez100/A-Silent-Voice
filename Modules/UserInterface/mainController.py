
from PyQt5.QtGui import QImage, QPixmap, QIcon, QMovie
import PyQt5.QtGui as gui
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot, Qt
import cv2
from Modules.ProcessImage import drawBoundingRectangle, extractRegionofInterest
import Modules.RecognitionThread as rt
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from Modules.UserInterface.quitController import QuitPrompt
from Modules.UserInterface.firsttime_prompt import FirstTimePrompt

class Thread(QThread):
    changePixmap = pyqtSignal(QImage, str)
    def __init__(self, model):
        super(Thread, self).__init__()
        self.thread = rt.Recoginize(model)
        self.thread.start()

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            frame = drawBoundingRectangle(frame)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            frame = extractRegionofInterest(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.thread.predict(frame)
            letter, acc = self.thread.getPrediction()
            #print('letter:',letter)
            self.changePixmap.emit(p, letter)

class MainForm(QMainWindow):
    def __init__(self, logWindow, model):
        super().__init__()
        loadUi('main_window.ui', self)
        self.tab_history = [0]
        #self.camera = cv2.VideoCapture(0)
        self.stackedWidget.setCurrentIndex(2)
        self.j_gesture = QMovie("Icons/alphabet/J.gif")
        self.jLabel.setMovie(self.j_gesture)
        self.z_gesture = QMovie("Icons/alphabet/Z.gif")
        self.zLabel.setMovie(self.z_gesture)
        self.logoutButton.clicked.connect(self.logoutAction)
        self.homeButton.clicked.connect(self.showHomePage)
        self.helpButton.clicked.connect(self.showHelp)
        self.aboutButton.clicked.connect(self.showAbout)
        self.quitButton.clicked.connect(self.logoutAction)
        self.hideButton.clicked.connect(self.showMinimized)
        self.minmaxButton.clicked.connect(self.minmaxWindow)
        self.backButton_1.clicked.connect(self.backFunction)
        self.backButton_2.clicked.connect(self.backFunction)
        self.backButton_3.clicked.connect(self.backFunction)
        self.backButton_4.clicked.connect(self.backFunction)
        self.aslButton.clicked.connect(self.showASL)
        self.A_button.clicked.connect(self.showLetterA)
        self.B_button.clicked.connect(self.showLetterB)
        self.C_button.clicked.connect(self.showLetterC)
        self.D_button.clicked.connect(self.showLetterD)
        self.E_button.clicked.connect(self.showLetterE)
        self.F_button.clicked.connect(self.showLetterF)
        self.G_button.clicked.connect(self.showLetterG)
        self.H_button.clicked.connect(self.showLetterH)
        self.I_button.clicked.connect(self.showLetterI)
        self.J_button.clicked.connect(self.showLetterJ)
        self.K_button.clicked.connect(self.showLetterK)
        self.L_button.clicked.connect(self.showLetterL)
        self.M_button.clicked.connect(self.showLetterM)
        self.N_button.clicked.connect(self.showLetterN)
        self.O_button.clicked.connect(self.showLetterO)
        self.P_button.clicked.connect(self.showLetterP)
        self.Q_button.clicked.connect(self.showLetterQ)
        self.R_button.clicked.connect(self.showLetterR)
        self.S_button.clicked.connect(self.showLetterS)
        self.T_button.clicked.connect(self.showLetterT)
        self.U_button.clicked.connect(self.showLetterU)
        self.V_button.clicked.connect(self.showLetterV)
        self.W_button.clicked.connect(self.showLetterW)
        self.X_button.clicked.connect(self.showLetterX)
        self.Y_button.clicked.connect(self.showLetterY)
        self.Z_button.clicked.connect(self.showLetterZ)
        self.thread = Thread(model)
        self.thread.changePixmap.connect(self.setImage)
        self.loginWindow = logWindow
        self.first_launch = True


    #def setFormWords(self):

    def event(self, ev):
        if type(ev) == gui.QShowEvent:
            self.thread.start()
        return super(MainForm, self).event(ev)

    def minmaxWindow(self):
        if self.minmaxButton.isChecked():
            self.showMaximized()
        else:
            self.showNormal()

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)

    @pyqtSlot(QImage, str)
    def setImage(self, image, letter):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))
        self.letterLabel.setText("Recognized Letter: "+letter)

    def showHomePage(self):
        if self.first_launch:
            self.openFirstTimeDialog()
            self.first_launch = False
        if self.tab_history[-1] != 0:
            self.tab_history.append(0)
        self.stackedWidget.setCurrentIndex(0)
        print(self.tab_history)

    def showASL(self):
        if self.tab_history[-1] != 1:
            self.tab_history.append(1)
        self.stackedWidget.setCurrentIndex(1)

    def showHelp(self):
        if self.tab_history[-1] != 2:
            self.tab_history.append(2)
        self.stackedWidget.setCurrentIndex(2)

    def showAbout(self):
        if self.tab_history[-1] != 3:
            self.tab_history.append(3)
        self.stackedWidget.setCurrentIndex(3)

    def showLetterA(self):
        self.alphabetStacked.setCurrentIndex(0)

    def showLetterB(self):
        self.alphabetStacked.setCurrentIndex(1)

    def showLetterC(self):
        self.alphabetStacked.setCurrentIndex(2)

    def showLetterD(self):
        self.alphabetStacked.setCurrentIndex(3)

    def showLetterE(self):
        self.alphabetStacked.setCurrentIndex(4)

    def showLetterF(self):
        self.alphabetStacked.setCurrentIndex(5)

    def showLetterG(self):
        self.alphabetStacked.setCurrentIndex(6)

    def showLetterH(self):
        self.alphabetStacked.setCurrentIndex(7)

    def showLetterI(self):
        self.alphabetStacked.setCurrentIndex(8)

    def showLetterJ(self):
        self.j_gesture.stop()
        self.j_gesture.start()
        self.alphabetStacked.setCurrentIndex(9)

    def showLetterK(self):
        self.alphabetStacked.setCurrentIndex(10)

    def showLetterL(self):
        self.alphabetStacked.setCurrentIndex(11)

    def showLetterM(self):
        self.alphabetStacked.setCurrentIndex(12)

    def showLetterN(self):
        self.alphabetStacked.setCurrentIndex(13)

    def showLetterO(self):
        self.alphabetStacked.setCurrentIndex(14)

    def showLetterP(self):
        self.alphabetStacked.setCurrentIndex(15)

    def showLetterQ(self):
        self.alphabetStacked.setCurrentIndex(16)

    def showLetterR(self):
        self.alphabetStacked.setCurrentIndex(17)

    def showLetterS(self):
        self.alphabetStacked.setCurrentIndex(18)

    def showLetterT(self):
        self.alphabetStacked.setCurrentIndex(19)

    def showLetterU(self):
        self.alphabetStacked.setCurrentIndex(20)

    def showLetterV(self):
        self.alphabetStacked.setCurrentIndex(21)

    def showLetterW(self):
        self.alphabetStacked.setCurrentIndex(22)

    def showLetterX(self):
        self.alphabetStacked.setCurrentIndex(23)

    def showLetterY(self):
        self.alphabetStacked.setCurrentIndex(24)

    def showLetterZ(self):
        self.z_gesture.stop()
        self.z_gesture.start()
        self.alphabetStacked.setCurrentIndex(25)

    @pyqtSlot()
    def logoutAction(self):
        #self.close()
        self.openQuitDialog()
        #self.loginWindow.show()

    def openQuitDialog(self):
        self.window = QuitPrompt(self)
        self.window.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.window.show()

    def openFirstTimeDialog(self):
        self.window = FirstTimePrompt(self)
        self.window.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)
        self.window.show()

    def backFunction(self):
        if len(self.tab_history) != 1:
            self.tab_history.pop(-1)
            self.stackedWidget.setCurrentIndex(self.tab_history[-1])
            if self.tab_history[-1] == 0:
                self.homeButton.setChecked(True)
            elif self.tab_history[-1] == 1:
                self.aslButton.setChecked(True)
            elif self.tab_history[-1] == 2:
                self.helpButton.setChecked(True)
            elif self.tab_history[-1] == 3:
                self.aboutButton.setChecked(True)