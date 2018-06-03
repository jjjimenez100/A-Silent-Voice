from pathlib import Path
import cv2
import numpy
import os
import time
import platform

# Constants

# FPS of video capturing device
FRAME_RATE = 7
OPERATING_SYSTEM = platform.system()
# Get the current working directory of the python file
PATH = os.path.dirname(os.path.realpath(__file__))
FRAMES_SAVE_PATH = PATH + "\\frames\\"
PREVIOUS_TIME = 0
# Enable or disable printing of texts on console to help with debugging
DEBUG_MODE = True

BACKGROUND_MODEL = cv2.createBackgroundSubtractorKNN(5000, 20)

# Region of interest, the bounding rectangle constants
RECT_BEGIN_X = 0.5
RECT_BEGIN_Y = 0.8

# Blur value constant using KNN Gaussian
BLUR_VALUE = 41

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

# Initializes video recording given the specified recording type.
# type 0 = taking snapshots every n seconds
# type 1 = take snapshots every frame
# type 2 = take snapshots only if a certain key was pressed by the user, indicated by the 64bit ascii code
# recognitionFunction - function to be executed after capture a single frame snapshot
# e.g: the recognition algorithm
# The default exit key is "esc"
def initVideoRecording(device: cv2.VideoCapture, type=0, snapshotTime=0, recognitionFunction=0, captureKey=99):
    device.set(cv2.CAP_PROP_FPS, FRAME_RATE)
    if(type == 0):
        timeBasedRecording(device, snapshotTime)
    elif(type == 1):
        frameByFrameRecording(device)
    elif(type == 2):
        userInteractedRecording(device, captureKey)

#  Take snapshots from video recording every n seconds
def timeBasedRecording(device: cv2.VideoCapture, snapshotTime: int, recognitionFunction=0):
    # Keep track of total frame #
    count = 0
    # Predict frames per second
    frameCount = 0
    if(DEBUG_MODE):
        setInitialTime()
    while(True):
        isRecording, snapshot = device.read()
        frameCount += 1
        noBackground = removeBackground(snapshot)
        if frameCount == (FRAME_RATE * snapshotTime):
            frameCount = 0
            regionOfInterest = extractRegionofInterest(noBackground)
            grayscaleROI = convertToGrayscale(regionOfInterest)
            blurROI = blurImage(grayscaleROI)
            saveImage(blurROI, (FRAMES_SAVE_PATH + "frame" + str(count)))
        count += 1
        if(not recognitionFunction == 0):
            control = recognitionFunction()
        drawBoundingRectangle(snapshot)
        displayImage(snapshot, "Original")
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    if(DEBUG_MODE):
        prettyPrintElapsedTime()

# Take snapshots every video frame
def frameByFrameRecording(device: cv2.VideoCapture, recognitionFunction=0):
    count = 0
    if (DEBUG_MODE):
        setInitialTime()
    while (True):
        isRecording, snapshot = device.read()
        regionOfInterest = extractRegionofInterest(removeBackground(snapshot))
        grayscaleROI = convertToGrayscale(regionOfInterest)
        blurROI = blurImage(grayscaleROI)
        saveImage(blurROI, (FRAMES_SAVE_PATH + "frame" + str(count)))
        count += 1
        #if (not recognitionFunction == 0):
            #control = recognitionFunction()
        drawBoundingRectangle(snapshot)
        displayImage(snapshot, "Original")
        k = cv2.waitKey(30) & 0xff
        if(k==27):
            break
    if (DEBUG_MODE):
        prettyPrintElapsedTime()

# Take snapshots only if a certain key was pressed
def userInteractedRecording(device: cv2.VideoCapture, captureKey, recognitionFunction=0):
    count = 0
    if (DEBUG_MODE):
        setInitialTime()
    while (True):
        isRecording, snapshot = device.read()
        noBackground = removeBackground(snapshot)
        # if (not recognitionFunction == 0):
        # control = recognitionFunction()
        drawBoundingRectangle(snapshot)
        displayImage(snapshot, "Original")
        k = cv2.waitKey(30) & 0xff
        if (k == 27):
            break
        if (k == captureKey):
            regionOfInterest = extractRegionofInterest(removeBackground(noBackground))
            grayscaleROI = convertToGrayscale(regionOfInterest)
            blurROI = blurImage(grayscaleROI)
            saveImage(blurROI, (FRAMES_SAVE_PATH + "frame" + str(count)))
            print("Captured frame %d", (count))
            count += 1
    if (DEBUG_MODE):
        prettyPrintElapsedTime()

# Convert a given image to its grayscale equivalent
def convertToGrayscale(snapshot):
    return cv2.cvtColor(snapshot, cv2.COLOR_BGR2GRAY)

# Draw a bounding rectangle on the image, specified by the RECT_BEGIN constants
def drawBoundingRectangle(snapshot):
    return cv2.rectangle(snapshot, (int(RECT_BEGIN_X * snapshot.shape[1]), 0),
                  (snapshot.shape[1], int(RECT_BEGIN_Y * snapshot.shape[0])), (255, 0, 0), 2)

# Extract region of interest specified by the bounding rectangle.
def extractRegionofInterest(snapshot):
    return snapshot[0:int(RECT_BEGIN_Y * snapshot.shape[0]),
              int(RECT_BEGIN_X * snapshot.shape[1]):snapshot.shape[1]]

# Try to smooth the given image by blurring it out
def blurImage(regionOfInterest):
    return cv2.GaussianBlur(regionOfInterest, (BLUR_VALUE, BLUR_VALUE), 0)

# Remove unnecessary noise and background
def removeBackground(frame):
    foregroundMask = BACKGROUND_MODEL.apply(frame)
    # White rectangle
    kernel = numpy.ones((3, 3), numpy.uint8)
    # Convolve it with the mask
    # Two iteration of erosion provides better results
    foregroundMask = cv2.erode(foregroundMask, kernel, iterations=2)
    return cv2.bitwise_and(frame, frame, mask=foregroundMask)

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

# Get current system time
def getTime():
    if(OPERATING_SYSTEM == "Windows"):
        return time.clock()
    else:
        return time.time()

# Utilized for measuring the actual performance of the code
def setInitialTime():
    PREVIOUS_TIME = getTime()

# Actual runtime
def getElapsedTime():
    return getTime() - PREVIOUS_TIME

# Print elapsed time in a human readable seconds format
def prettyPrintElapsedTime():
    print(time.strftime("%H:%M:%S", time.gmtime(getElapsedTime())))

def main():
    enableCVOptimizations()
    initVideoRecording(initDevice(), 2)

# Init a silent voice project
if(__name__ == "__main__"):
    main()