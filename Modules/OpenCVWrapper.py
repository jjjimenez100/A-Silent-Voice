from pathlib import Path
import cv2, numpy, os, time, platform

# Check if given file exists
# Returns: True if the specified file path exists
# Throws a FileNotFoundError otherwise
def fileExists(fileName: str):
    if(Path(fileName).is_file()):
        return True
    else:
        raise FileNotFoundError

# Check if given directory exists
# Returns: True if the specified directory path exists
# Throws a NotADirectoryError otherwise
def directoryExists(directoryName: str):
    if(Path(directoryName).is_dir()):
        return True
    else:
        raise NotADirectoryError

# Load an image with a given file path, default mode is 0.
# 0 - load grayscale image, 1 - default, -1 include alpha channels
# Returns: an image represented by a numpy.ndarray if specified file path is valid
# Otherwise, refer to fileExists function
def loadImage(fileName: str, isGrayScale=0) -> numpy.ndarray:
    if(fileExists(fileName)):
        return cv2.imread(fileName, isGrayScale)

# Display a captioned window containing the given image.
def displayImage(image: numpy.ndarray, caption: str):
    cv2.imshow(caption, image)

# Saves the image with the given file extension
def saveImage(image: numpy.ndarray, fileName: str, fileExtension=".png"):
    cv2.imwrite((fileName+fileExtension), image)

# Initializes video capturing device. Default deviceId is 0.
# First one attached is labeled as 0, second as 1, etc..
def initDevice(deviceId=0):
    device = cv2.VideoCapture(deviceId)
    # According to opencv docs, there are instances that the video stream
    # is not initialized automatically.
    if (not device.isOpened()):
        device.open(deviceId)

    return device

# Convert a given image to its grayscale equivalent
def convertToGrayscale(snapshot):
    return cv2.cvtColor(snapshot, cv2.COLOR_BGR2GRAY)

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

# Add two image matrices
def addImages(imageOne: numpy.ndarray, imageTwo: numpy.ndarray):
    return cv2.add(imageOne, imageTwo)

# Subtract two image matrices
def subtractImages(imageOne: numpy.ndarray, imageTwo: numpy.ndarray):
    return cv2.subtract(imageOne, imageTwo)

# Convert a given image to its HSV equivalent
def convertToHSV(image: numpy.ndarray):
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Upscale an image given a new value for its row and columns
def upsizeImage(image: numpy.ndarray, col: int, row: int):
    return cv2.pyrUp(image, dstsize=(col, row))

# Downscale an image given a new value for its row and columns
def downsizeImage(image: numpy.ndarray, col: int, row: int):
    return cv2.pyrDown(image, dstsize=(col, row))

def resizeImage(image: numpy.ndarray, col: int, row: int):
    return cv2.resize(image, (col, row))

# Create a KNN Background Subtractor model from opencv
def createKNNBackgroundSubtractor(history: int, threshold: int):
    return cv2.createBackgroundSubtractorKNN(history, threshold)
