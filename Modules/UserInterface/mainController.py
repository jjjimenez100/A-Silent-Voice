
from PyQt5.QtGui import QImage, QPixmap, QIcon
import PyQt5.QtGui as gui
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot, Qt
import cv2
from Modules.ProcessImage import drawBoundingRectangle, extractRegionofInterest, convertToGrayscale
import iconpack
import Modules.RecognitionThread as rt
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import Modules.WordBuilder as wb
import Modules.UserInterface.RunBatchFile as rbf
import sys

class Thread(QThread):
    changePixmap = pyqtSignal(QImage, str, float)
    def __init__(self, model, fps=7, camera=0):
        super(Thread, self).__init__()
        self.thread = rt.Recoginize(model)
        self.thread.daemon =  True
        self.fps = fps
        self.camera = camera

    def run(self):
        self.thread.start()
        print(self.camera)
        cap = cv2.VideoCapture(self.camera)
        cap.set(cv2.CAP_PROP_FPS, self.fps)
        while True:
            ret, frame = cap.read()
            frame = drawBoundingRectangle(frame)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            frame = extractRegionofInterest(frame)
            frame = convertToGrayscale(frame)
            self.thread.predict(frame)
            letter, acc = self.thread.getPrediction()
            self.changePixmap.emit(p, letter, acc)

class MainForm(QMainWindow):
    def __init__(self, logWindow, model, cameraCount):
        super().__init__()
        loadUi('main_window.ui', self)
        #self.camera = cv2.VideoCapture(0)
        self.stackedWidget.setCurrentIndex(3)
        self.logoutButton.clicked.connect(self.logoutAction)
        self.homeButton.clicked.connect(self.showHomePage)
        self.settingsButton.clicked.connect(self.showSettingsPage)
        self.helpButton.clicked.connect(self.showHelp)
        self.aboutButton.clicked.connect(self.showAbout)
        self.quitButton.clicked.connect(self.logoutAction)
        self.hideButton.clicked.connect(self.showMinimized)
        self.minmaxButton.clicked.connect(self.minmaxWindow)
        self.fixInstallationButton.clicked.connect(self.fixInstallation)
        self.speakingRateSlider.valueChanged.connect(self.sliderValueChange)
        self.speakingVolumeSlider.valueChanged.connect(self.sliderValueChange)
        self.formWordCheckbox.stateChanged.connect(self.checkCheckBoxes)
        self.showAccuracyCheckbox.stateChanged.connect(self.checkCheckBoxes)
        self.speakingVolumeMuteCheckbox.stateChanged.connect(self.checkCheckBoxes)
        # self.speakerDeviceCombobox.currentIndexChanged.connect(self.onComboBoxChange) nonexistant cuz im a scrub
        self.cameraDeviceCombobox.currentIndexChanged.connect(self.onComboBoxChange)
        self.cameraFPSCombobox.currentIndexChanged.connect(self.onComboBoxChange)
        self.recognitionSpeedComboBox.currentIndexChanged.connect(self.onComboBoxChange)
        print("WALAO")

        self.wordBuilder = wb.WordBuilder()
        self.model = model
        self.loginWindow = logWindow
        self.rate = 0
        self.volume = 0
        self.fps = 7
        self.speed = 1
        self.showAcc = False
        self.showWord = False
        self.cameraCount = cameraCount
        self.cameraDevice = 0

        self.setComboBoxes()
        print("WALAO")
        self.createThread()

        #def setFormWords(self):
    def createThread(self, fps=7, camera=0):
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
        self.wordBuilder.sayWord()
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
        self.stackedWidget.setCurrentIndex(0)

    def showSettingsPage(self):
        self.stackedWidget.setCurrentIndex(1)

    def showHelp(self):
        self.stackedWidget.setCurrentIndex(2)

    def showAbout(self):
        self.stackedWidget.setCurrentIndex(3)

    @pyqtSlot()
    def logoutAction(self):
        self.close()
        self.loginWindow.show()
