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
    control = True
    while(control):
        count = 0
        isRecording = True
        while(isRecording):
            device.set(cv2.CAP_PROP_POS_MSEC, (count * snapshotTime))
            isRecording, snapshot = device.read()
            saveImage(snapshot, directory + "\\frame%d" % count)
            count += 1
        if(not recognitionFunction == 0):
            control = recognitionFunction()

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

# Todo: Image processing modules