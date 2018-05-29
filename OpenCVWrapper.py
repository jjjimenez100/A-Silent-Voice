from pathlib import Path
import cv2
import numpy

def fileExists(fileName: str):
    if(Path(fileName).is_file()):
        return True
    else:
        raise FileNotFoundError

def directoryExists(directoryName: str):
    if(Path(directoryName).is_dir()):
        return True
    else:
        raise NotADirectoryError

# 0 - load grayscale image, 1 - default, -1 include alpha channels
def loadImage(fileName: str, isGrayScale=0) -> numpy.ndarray:
    if(fileExists(fileName)):
        return cv2.imread(fileName, isGrayScale)

# Returns the key pressed during the elapsed given time
# Default is -1 if nothing was pressed
def displayImage(image: numpy.ndarray, caption: str, time=0) -> int:
    cv2.imshow(caption, image)
    return cv2.waitKey(time)

# Saves the image with the given file extension
def saveImage(image: numpy.ndarray, fileName: str, fileExtension=".png"):
    cv2.imwrite((fileName+fileExtension), image)

# Which camera device to use. First one attached is labeled as 0, second as 1, etc..
def initDevice(deviceId=0):
    device = cv2.VideoCapture(deviceId)
    # According to opencv docs, there are instances that the video stream
    # is not initialized automatically.
    if (not device.isOpened()):
        device.open(deviceId)

    return device

# recognitionFunction - function to be executed after capture a single frame snapshot
# e.g: the recognition algorithm
def initVideoRecording(device: cv2.VideoCapture, snapshotTime: int, directory: str, recognitionFunction=0):
    frameRate = 8
    frameCount = 0
    device.set(cv2.CAP_PROP_FPS, frameRate)
    count = 0
    while(True):
        isRecording, snapshot = device.read()
        cv2.imshow("hahaha", snapshot)
        frameCount += 1
        if frameCount == (frameRate * snapshotTime):
            frameCount = 0
            saveImage(snapshot, "frame" + str(count))
            print("hi")
        count += 1
        if(not recognitionFunction == 0):
            control = recognitionFunction()
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

# https://docs.opencv.org/trunk/d8/dfe/classcv_1_1VideoCapture.html#aa6480e6972ef4c00d74814ec841a2939
def getVideoProperty(device : cv2.VideoCapture, propertyId):
    return device.get(propertyId)

# List of available video properties:
# https://docs.opencv.org/trunk/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
# Change video width, height, playback etc.
def changeVideoProperty(device : cv2.VideoCapture, propertyId, newValue):
    device.set(propertyId, newValue)

# In case the compiled binaries are defaulted to False
def enableCVOptimizations():
    if(not cv2.useOptimized()):
        cv2.setUseOptimized(True)

def addImages(imageOne: numpy.ndarray, imageTwo: numpy.ndarray):
    return cv2.add(imageOne, imageTwo)

def subtractImages(imageOne: numpy.ndarray, imageTwo: numpy.ndarray):
    return cv2.subtract(imageOne, imageTwo)

def convertToHSV(image: numpy.ndarray):
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

## Upscale an image given a new value for its row and columns
def upsizeImage(image: numpy.ndarray, col: int, row: int):
    return cv2.pyrUp(image, dstsize=(col, row))

## Downscale an image given a new value for its row and columns
def downsizeImage(image: numpy.ndarray, col: int, row: int):
    return cv2.pyrDown(image, dstsize=(col, row))

# Todo: Image processing modules

initVideoRecording(initDevice(), 2, "")