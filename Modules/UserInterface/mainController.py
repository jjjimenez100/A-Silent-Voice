from PyQt5.QtGui import QImage, QPixmap, QIcon
import PyQt5.QtGui as gui
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot, Qt
import cv2
from Modules.ProcessImage import drawBoundingRectangle, extractRegionofInterest, convertToGrayscale
import Modules.UserInterface.iconpack
import Modules.RecognitionThread as rt
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import Modules.WordBuilder as wb
import Modules.UserInterface.RunBatchFile as rbf
import sys, os, queue

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
        self.queue = queue.Queue()
        self.thread = rt.Recoginize(model, self.queue)
        self.thread.daemon = True
        self.fps = fps
        self.camera = camera
        self.cap = cv2.VideoCapture

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
            frame = extractRegionofInterest(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.thread.predict(frame)
            letter, acc = self.thread.getPrediction()
            #print('letter:',letter)
            self.changePixmap.emit(p, letter)

class MainForm(QMainWindow):
    def __init__(self, model, cameraCount):
        super().__init__()
        if getattr(sys, 'frozen', False):
            ui = 'main_window.ui'
            loadUi(resource_path(ui), self)
        else:
            ui = 'Modules/UserInterface/main_window.ui'
            loadUi(ui, self)
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
        self.formWordCheckbox.stateChanged.connect(self.checkCheckBoxes)
        self.showAccuracyCheckbox.stateChanged.connect(self.checkCheckBoxes)

        self.wordBuilder = wb.WordBuilder()
        self.model = model
        self.showAcc = False
        self.showWord = False
        self.cameraCount = cameraCount
        self.cameraDevice = 0

        self.setComboBoxes()
        self.createThread()

        #def setFormWords(self):
    def createThread(self, fps=7, camera=0):
        if self.cameraCount > 0:
            self.thread = Thread(self.model, fps, camera)
            self.thread.changePixmap.connect(self.setImage)
            self.thread.start()

    def fixInstallation(self):
        rbf.install()

    def setComboBoxes(self):
        for i in range(7,16):
            self.cameraFPSCombobox.addItem(str(i))
        self.recognitionSpeedComboBox.addItems(["1 - Fastest", "2 - Normal", "3 - Slowest"])

        if self.cameraCount>0:
            self.cameraDeviceCombobox.addItem("Primary Camera")
            if self.cameraCount>1:
                self.cameraDeviceCombobox.addItem("Secondary Camera")
        else:
            self.cameraDeviceCombobox.addItem("NO CAMERA DETECTED")
        self.speakerDeviceCombobox.addItem("DEFAULT OUTPUT DEVICE")

    def onComboBoxChange(self):
        self.fps = self.cameraFPSCombobox.currentText()
        self.speed = self.recognitionSpeedComboBox.currentText()
        cam = self.cameraDeviceCombobox.currentText()
        if cam == "Primary Camera":
            cam = 0
        elif cam == "Secondary Camera":
            cam = 1
        self.cameraDevice = cam
        self.thread.terminate()
        self.thread.wait()
        if self.thread.isFinished():
            self.createThread(int(self.fps), cam)

    def sliderValueChange(self):
        self.rate = self.speakingRateSlider.value()
        self.volume = self.speakingVolumeSlider.value()/100
        self.audioinvolumeLabel.setText(str(self.rate*5)+" WPM")
        self.audiooutvolumeLabel.setText(str(self.volume*100)+"%")
        self.wordBuilder.changeVolume(self.volume)
        self.wordBuilder.changeRate(self.rate*5)

    def sayWord(self):
        if self.wordBuilder.sayWord():
            self.wordBuilder.setWord("")

    def removeLetter(self):
        word = self.wordBuilder.getWord()
        if word:
            self.wordBuilder.setWord(word[:-1])

    def keyPressEvent(self, evt):
        if type(evt) == gui.QKeyEvent:
            if evt.key() == Qt.Key_Return:
                self.sayWord()

            elif evt.key() == Qt.Key_Backspace:
                self.removeLetter()


    def checkCheckBoxes(self):
        if self.speakingVolumeMuteCheckbox.isChecked():
            self.wordBuilder.changeVolume(0)
        else:
            self.wordBuilder.changeVolume(self.volume)
        if self.showAccuracyCheckbox.isChecked():
            self.showAcc = True
        else:
            self.showAcc = False
        if self.formWordCheckbox.isChecked():
            self.showWord = True
        else:
            self.showWord = False

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

    @pyqtSlot(QImage, str, float)
    def setImage(self, image, letter, acc):
        word = ''
        if self.showWord:
            word = self.wordBuilder.checkLetter(letter)
        self.videoLabel.setPixmap(QPixmap.fromImage(image))
        if self.showAcc:
            self.letterLabel.setText("Recognized Letter: "+letter+" - "+str(round(acc*100,2))+"%"+"\t"+word)
        else:
            self.letterLabel.setText("Recognized Letter: "+letter+"\t"+word)

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
		self.thread.cap.release()
        self.thread.terminate()
        self.thread.wait()
        self.close()
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
