from PyQt5.QtGui import QImage, QPixmap, QMovie
import PyQt5.QtGui as gui
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot, Qt
import cv2
from PyQt5.uic.properties import QtGui

from Modules.ProcessImage import drawBoundingRectangle, extractRegionofInterest, convertToGrayscale
import Modules.UserInterface.iconpack
import Modules.RecognitionThread as rt
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import Modules.WordBuilder as wb
import sys, os

from Modules.UserInterface.firsttime_guide import FirstTimeGuide
from Modules.UserInterface.quitController import QuitPrompt
from Modules.UserInterface.firsttime_prompt import FirstTimePrompt

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Thread(QThread):
    changePixmap = pyqtSignal(QImage, str, float)
    def __init__(self, model, fps=7, camera=0,):# recognitionThread=rt.Recoginize):
        super(Thread, self).__init__()
        self.thread = rt.Recoginize(model)
        self.thread.daemon = True
        self.fps = fps
        self.camera = camera
        self.cap = ''

    def run(self):
        self.thread.start()
        self.cap = cv2.VideoCapture(self.camera)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        while True:
            ret, frame = self.cap.read()
            frame = cv2.flip(frame, 1)
            roi = extractRegionofInterest(frame)
            gs = convertToGrayscale(roi)
            self.thread.predict(gs)
            # self.queue.put(gs)
            rect = drawBoundingRectangle(frame)
            rgbImage = cv2.cvtColor(rect, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            # frame = extractRegionofInterest(frame)
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # self.thread.predict(frame)
            letter, acc = self.thread.getPrediction()
            #print('letter:',letter)
            self.changePixmap.emit(p, letter, acc)

class MainForm(QMainWindow):
    def __init__(self, model, cameraCount):
        print("mf")
        super().__init__()
        if getattr(sys, 'frozen', False):
            ui = 'main_window.ui'
            loadUi(resource_path(ui), self)
            self.j_gesture = QMovie(resource_path("Icons/alphabet/J.gif"))
            self.z_gesture = QMovie(resource_path("Icons/alphabet/Z.gif"))
        else:
            ui = 'Modules/UserInterface/main_window.ui'
            loadUi(ui, self)
            self.j_gesture = QMovie("Modules/UserInterface/Icons/alphabet/J.gif")
            self.z_gesture = QMovie("Modules/UserInterface/Icons/alphabet/Z.gif")
        self.tab_history = [0]
        #self.camera = cv2.VideoCapture(0)
        self.stackedWidget.setCurrentIndex(0)
        self.jLabel.setMovie(self.j_gesture)
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
        self.A_button.clicked.connect(lambda: self.showLetters(0))
        self.B_button.clicked.connect(lambda: self.showLetters(1))
        self.C_button.clicked.connect(lambda: self.showLetters(2))
        self.D_button.clicked.connect(lambda: self.showLetters(3))
        self.E_button.clicked.connect(lambda: self.showLetters(4))
        self.F_button.clicked.connect(lambda: self.showLetters(5))
        self.G_button.clicked.connect(lambda: self.showLetters(6))
        self.H_button.clicked.connect(lambda: self.showLetters(7))
        self.I_button.clicked.connect(lambda: self.showLetters(8))
        self.J_button.clicked.connect(lambda: self.showLetters(9))
        self.K_button.clicked.connect(lambda: self.showLetters(10))
        self.L_button.clicked.connect(lambda: self.showLetters(11))
        self.M_button.clicked.connect(lambda: self.showLetters(12))
        self.N_button.clicked.connect(lambda: self.showLetters(13))
        self.O_button.clicked.connect(lambda: self.showLetters(14))
        self.P_button.clicked.connect(lambda: self.showLetters(15))
        self.Q_button.clicked.connect(lambda: self.showLetters(16))
        self.R_button.clicked.connect(lambda: self.showLetters(17))
        self.S_button.clicked.connect(lambda: self.showLetters(18))
        self.T_button.clicked.connect(lambda: self.showLetters(19))
        self.U_button.clicked.connect(lambda: self.showLetters(20))
        self.V_button.clicked.connect(lambda: self.showLetters(21))
        self.W_button.clicked.connect(lambda: self.showLetters(22))
        self.X_button.clicked.connect(lambda: self.showLetters(23))
        self.Y_button.clicked.connect(lambda: self.showLetters(24))
        self.Z_button.clicked.connect(lambda: self.showLetters(25))
        self.thread = Thread(model)
        self.thread.changePixmap.connect(self.setImage)
        self.formWordCheckbox.stateChanged.connect(self.checkCheckBoxes)
        self.showAccuracyCheckbox.stateChanged.connect(self.checkCheckBoxes)

        self.wordBuilder = wb.WordBuilder()
        self.model = model
        self.showAcc = False
        self.showWord = False
        self.cameraCount = cameraCount
        self.cameraDevice = 0

        self.originial_buttons = self.aslButton.styleSheet()
        self.originial_home = self.homePage.styleSheet()
        self.original_label = self.letterFrame.styleSheet()
        self.original_video = self.videoLabel.styleSheet()
        self.original_checkbox = self.formWordCheckbox.styleSheet()
        self.tutorial_stylesheet = "border: 3.5px solid red;"

        #self.setComboBoxes()
        self.createThread()
        #def setFormWords(self):
        self.center(self)

    def createThread(self, fps=7, camera=0):
        if self.cameraCount > 0:
            self.thread = Thread(self.model, fps, camera)
            self.thread.changePixmap.connect(self.setImage)
            self.thread.start()

    def firsttime_tutorial(self, number):
        if number == 0:
            self.stackedWidget.setCurrentIndex(0)
            self.homeButton.setStyleSheet(self.originial_buttons + self.tutorial_stylesheet)
            self.aslButton.setStyleSheet(self.originial_buttons + self.tutorial_stylesheet)
            self.helpButton.setStyleSheet(self.originial_buttons + self.tutorial_stylesheet)
            self.aboutButton.setStyleSheet(self.originial_buttons + self.tutorial_stylesheet)
            self.logoutButton.setStyleSheet(self.originial_buttons + self.tutorial_stylesheet)
        else:
            self.homeButton.setStyleSheet(self.originial_buttons)
            self.aslButton.setStyleSheet(self.originial_buttons)
            self.helpButton.setStyleSheet(self.originial_buttons)
            self.aboutButton.setStyleSheet(self.originial_buttons)
            self.logoutButton.setStyleSheet(self.originial_buttons)
        if number == 1:
            self.stackedWidget.setCurrentIndex(0)
            self.homeButton.setStyleSheet(self.originial_buttons + self.tutorial_stylesheet)
        else:
            self.homeButton.setStyleSheet(self.originial_buttons)
        if number == 2:
            self.stackedWidget.setCurrentIndex(1)
            self.aslButton.setStyleSheet(self.originial_buttons + self.tutorial_stylesheet)
        else:
            self.aslButton.setStyleSheet(self.originial_buttons)
        if number == 3 or number == 11:
            self.stackedWidget.setCurrentIndex(2)
            self.helpButton.setStyleSheet(self.originial_buttons + self.tutorial_stylesheet)
        else:
            self.helpButton.setStyleSheet(self.originial_buttons)
        if number == 4:
            self.stackedWidget.setCurrentIndex(3)
            self.aboutButton.setStyleSheet(self.originial_buttons + self.tutorial_stylesheet)
        else:
            self.aboutButton.setStyleSheet(self.originial_buttons)
        if number == 5:
            self.stackedWidget.setCurrentIndex(0)
            self.logoutButton.setStyleSheet(self.originial_buttons + self.tutorial_stylesheet)
        else:
            self.logoutButton.setStyleSheet(self.originial_buttons)
        if number == 6:
            self.stackedWidget.setCurrentIndex(0)
            self.homePage.setStyleSheet(self.originial_home + self.tutorial_stylesheet)
        else:
            self.homePage.setStyleSheet(self.originial_home)
        if number == 7:
            self.stackedWidget.setCurrentIndex(0)
            self.letterFrame.setStyleSheet(self.original_label + self.tutorial_stylesheet)
        else:
            self.letterFrame.setStyleSheet(self.original_label)
        if number == 8:
            self.stackedWidget.setCurrentIndex(0)
            self.videoLabel.setStyleSheet(self.original_video + self.tutorial_stylesheet)
        else:
            self.videoLabel.setStyleSheet(self.original_video)
        if number == 9:
            self.stackedWidget.setCurrentIndex(0)
            self.formWordCheckbox.setStyleSheet(self.original_checkbox + self.tutorial_stylesheet)
        else:
            self.formWordCheckbox.setStyleSheet(self.original_checkbox)
        if number == 10:
            self.stackedWidget.setCurrentIndex(0)
            self.showAccuracyCheckbox.setStyleSheet(self.original_checkbox + self.tutorial_stylesheet)
        else:
            self.showAccuracyCheckbox.setStyleSheet(self.original_checkbox)
        if number == 11:
            self.stackedWidget.setCurrentIndex(0)
            self.homeButton.setStyleSheet(self.originial_buttons)
            self.aslButton.setStyleSheet(self.originial_buttons)
            self.helpButton.setStyleSheet(self.originial_buttons)
            self.aboutButton.setStyleSheet(self.originial_buttons)
            self.logoutButton.setStyleSheet(self.originial_buttons)
            self.showAccuracyCheckbox.setStyleSheet(self.original_checkbox)
            self.formWordCheckbox.setStyleSheet(self.original_checkbox)
            self.videoLabel.setStyleSheet(self.original_video)
            self.letterFrame.setStyleSheet(self.original_label)
            self.homePage.setStyleSheet(self.originial_home)

    def removeLetter(self):
        word = self.wordBuilder.getWord()
        if word:
            self.wordBuilder.setWord(word[:-1])

    def keyPressEvent(self, evt):
        if type(evt) == gui.QKeyEvent:
            if evt.key() == Qt.Key_Backspace:
                self.removeLetter()

    def checkCheckBoxes(self):
        if self.showAccuracyCheckbox.isChecked():
            self.showAcc = True
        else:
            self.showAcc = False
        if self.formWordCheckbox.isChecked():
            self.showWord = True
        else:
            self.showWord = False
            self.wordBuilder.setWord("")

    def minmaxWindow(self):
        if self.minmaxButton.isChecked():
            self.showMaximized()
        else:
            self.showNormal()

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
            pass

    @pyqtSlot(QImage, str, float)
    def setImage(self, image, letter, acc):
        word = ''
        if self.showWord and self.tab_history[-1] == 0:
            word = self.wordBuilder.checkLetter(letter)
        self.videoLabel.setPixmap(QPixmap.fromImage(image))
        if self.showAcc:
            self.letterLabel.setText(letter+" - "+str(round(acc*100,2))+"%"+"\t"+word)
        else:
            self.letterLabel.setText(letter+"\t"+word)

    def center(self, window):
        qr = window.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        window.move(qr.topLeft())

    def center_popups(self, window):
        qr = window.frameGeometry()
        cp = self.availableGeometry().center()
        qr.moveCenter(cp)
        window.move(qr.topLeft())

    def showHomePage(self):
        self.stackedWidget.setCurrentIndex(0)
        if self.tab_history[-1] != 0:
            self.tab_history.append(0)

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

    def showLetters(self, index):
        print(index)
        if index == 9:
            self.j_gesture.stop()
            self.j_gesture.start()
            self.alphabetStacked.setCurrentIndex(index)
        elif index == 25:
            self.z_gesture.stop()
            self.z_gesture.start()
            self.alphabetStacked.setCurrentIndex(index)
        else:
            self.alphabetStacked.setCurrentIndex(index)

    @pyqtSlot()
    def logoutAction(self):
        if self.openQuitDialog():
            if self.thread.cap:
                self.thread.cap.release()
            self.thread.terminate()
            self.thread.wait()
            self.close()
            try:
                os.remove("img.jpg")
            except OSError:
                pass
        self.quitprompt.close()
        #self.close()
        #self.loginWindow.show()

    def openQuitDialog(self):
        self.quitprompt = QuitPrompt(self)
        self.quitprompt.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.center(self.quitprompt)
        self.quitprompt.exec_()
        return self.quitprompt.getButtonPressed()

    def openFirstTimeDialog(self):
        print("FTD")
        self.window = FirstTimePrompt(self)
        self.window.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)
        self.center(self.window)
        self.window.exec_()

    def startTutorial(self):
        self.tutorialPrompt = FirstTimeGuide(self)
        self.tutorialPrompt.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)
        self.center(self.tutorialPrompt)
        self.tutorialPrompt.exec_()

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
