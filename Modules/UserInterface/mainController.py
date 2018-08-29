from PyQt5.QtGui import QImage, QPixmap, QMovie
import PyQt5.QtGui as gui
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot, Qt
import cv2
import Modules.UserInterface.iconpack
from Modules.ProcessImage import drawBoundingRectangle, extractRegionofInterest, convertToGrayscale, showAcc, changeROIPlacement
import Modules.RecognitionThread as rt
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import Modules.WordBuilder as wb
import sys, os
import numpy as np

from Modules.UserInterface.firsttime_guide import FirstTimeGuide
from Modules.UserInterface.quitController import QuitPrompt
from Modules.UserInterface.firsttime_prompt import FirstTimePrompt
from Modules.UserInterface.webcam_disconnect import WebcamPrompt

from Modules.FileFinder import resource_path

# Seperate thread for image processing to not make the main thread freeze
class Thread(QThread):
    changePixmap = pyqtSignal(QImage, str, float)

    def __init__(self, model, fps=7, camera=0, ):
        super(Thread, self).__init__()
        self.thread = rt.Recoginize(model)
        self.thread.daemon = True
        self.fps = fps
        self.camera = camera
        self.cap = ''

    # Starts the thread
    def run(self):
        self.thread.start()
        self.cap = cv2.VideoCapture(self.camera)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        while True:
            try:
                acc = 0
                ret, frame = self.cap.read()
                frame = cv2.flip(frame, 1)
                roi = extractRegionofInterest(frame)
                gs = convertToGrayscale(roi)
                self.thread.predict(gs)
                letter, acc = self.thread.getPrediction()
                rect = drawBoundingRectangle(frame,acc)
                rgbImage = cv2.cvtColor(rect, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p, letter.upper(), acc)
            except Exception as ex:
                print('error', ex)
                rgbImage = np.zeros((640,480,3), np.uint8)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p, 'error', 0)
                break


# Main window for the user interface
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

        self.createThread()
        self.center(self)

    # Creates the thread for image processing and viewer
    def createThread(self, fps=7, camera=0):
        if self.cameraCount > 0:
            self.thread = Thread(self.model, fps, camera)
            self.thread.changePixmap.connect(self.setImage)
            self.thread.start()

    # Shows the first time tutorial on launch
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

    # Removes the letter in the word if form words is chosen
    def removeLetter(self):
        word = self.wordBuilder.getWord()
        if word:
            self.wordBuilder.setWord(word[:-1])

    # Gets the keypressed event
    # Current events are:
    #   BACKSPACE -> removeLetter()
    def keyPressEvent(self, evt):
        if type(evt) == gui.QKeyEvent:
            if evt.key() == Qt.Key_Backspace:
                self.removeLetter()
            elif self.tab_history[-1] == 1:
                for i in range(0, 26):
                    if evt.key() == i+65:
                        button = 'self.'+chr(i+65)+'_button.click()'
                        exec(button)


    # Checks the checkboxes in the Recognition tab and sets the values accordingly
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

    # Checks the window size to change the size of the window to normal or maximum
    def minmaxWindow(self):
        if self.minmaxButton.isChecked():
            self.showMaximized()
        else:
            self.showNormal()

    # Gets the mouse position every mouse click
    def mousePressEvent(self, event):
        self.offset = event.pos()

    # Gets the mouse position every mouse movement
    def mouseMoveEvent(self, event):
        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
        except:
            pass

    # Signal with the recognition thread to create a word or shows the accuracy
    # and passes it to the given labels in the user interface
    @pyqtSlot(QImage, str, float)
    def setImage(self, image, letter, acc):
        if letter == 'error':
            self.openWebcamDialog(1)
            return
        word = ''
        if self.showWord and self.tab_history[-1] == 0:
            word = self.wordBuilder.checkLetter(letter)
        self.videoLabel.setPixmap(QPixmap.fromImage(image))
        if self.showAcc:
            self.letterLabel.setText(letter)# + " - " + str(round(acc * 100, 2)) + "%")
            showAcc(True)
            self.wordLabel.setText(word)
        else:
            showAcc(False)
            self.letterLabel.setText(letter)
            self.wordLabel.setText(word)

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
        self.close()

    def openWebcamDialog(self, error_type):
        self.webcamPrompt = WebcamPrompt(self)
        if error_type == 1:
            self.webcamPrompt.change_label("Web-camera has been disconnected. Please restart the application.")
        else:
            self.webcamPrompt.change_label("No web-camera detected. Please close the application.")
        self.webcamPrompt.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.center(self.webcamPrompt)
        self.webcamPrompt.exec_()
        if error_type == 1:
            self.logoutAction()


    def openQuitDialog(self):
        self.quitprompt = QuitPrompt(self)
        self.quitprompt.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.center(self.quitprompt)
        self.quitprompt.exec_()
        return self.quitprompt.getButtonPressed()

    def openFirstTimeDialog(self):
        print("FTD")
        if not self.cameraCount > 0:
            self.openWebcamDialog('pls')
        else:
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

    def closeEvent(self, event):
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
        else:
            event.ignore()
        self.quitprompt.close()
