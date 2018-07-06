from Modules.OpenCVWrapper import *
import os, time, platform
from Modules.CNN.Constants import *
from keras.models import load_model

# Constants

# FPS of video capturing device
FRAME_RATE = 7
OPERATING_SYSTEM = platform.system()
# Get the current working directory of the python file
PATH = os.path.dirname(os.path.realpath(__file__))
FRAMES_SAVE_PATH = PATH + "\\Frames\\"
PREVIOUS_TIME = 0
# Enable or disable printing of texts on console to help with debugging
DEBUG_MODE = True

## Deprecated
# BACKGROUND_MODEL = createKNNBackgroundSubtractor(5000, 20)

# Uncomment for neural net
# CNN_MODEL = load_model(MODEL_PATH)

# Region of interest, the bounding rectangle constants
RECT_BEGIN_X = 0.5
RECT_BEGIN_Y = 0.8

# Blur value constant using KNN Gaussian
BLUR_VALUE = 41

# New background subtraction algorithm. Reduces pixel values that are in specified HSV range to 0, which is black.
def thresholdHSVBackground(image):
    l_h = cv2.getTrackbarPos('L - h', 'HSV Values')
    u_h = cv2.getTrackbarPos('U - h', 'HSV Values')
    l_s = cv2.getTrackbarPos('L - s', 'HSV Values')
    u_s = cv2.getTrackbarPos('U - s', 'HSV Values')
    l_v = cv2.getTrackbarPos('L - v', 'HSV Values')
    u_v = cv2.getTrackbarPos('U - v', 'HSV Values')

    MIN_HSV = numpy.array([l_h, l_s, l_v])
    MAX_HSV = numpy.array([u_h, u_s, u_v])

    imageMask = cv2.inRange(image, MIN_HSV, MAX_HSV)
    noBackground = cv2.bitwise_and(image, image, mask=imageMask)
    blurImage = cv2.medianBlur(cv2.GaussianBlur(noBackground, (11,11), 0), 15)
    # [0] - H, [1] - S, [2] - V
    greyscaleImage = numpy.dsplit(blurImage, blurImage.shape[-1])[2]
    ret, thresh = cv2.threshold(greyscaleImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh

# Function to create HSV trackbars
def createHSVTrackBars():
    createNewWindow("HSV Values")
    createTrackbar('L - h', 'HSV Values', 0, 179)
    createTrackbar('U - h', 'HSV Values', 179, 179)
    # Ideal value - 21
    createTrackbar('L - s', 'HSV Values', 0, 255)
    createTrackbar('U - s', 'HSV Values', 255, 255)

    createTrackbar('L - v', 'HSV Values', 0, 255)
    createTrackbar('U - v', 'HSV Values', 255, 255)

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
        # noBackground = removeBackground(snapshot)
        if frameCount == (FRAME_RATE * snapshotTime):
            frameCount = 0
            ###### regionOfInterest = extractRegionofInterest(snapshot)
            # grayscaleROI = convertToGrayscale(regionOfInterest)
            # blurROI = blurImage(grayscaleROI)
            noBackground = thresholdHSVBackground(snapshot)
            displayImage(noBackground, "no bg")
            # RECOGNITION FUNCTION GOES HERE. FEED THE getPrediction() FUNCTION WITH THE BLUR ROI IMAGE.
            # saveImage(blurROI, (FRAMES_SAVE_PATH + "frame" + str(count)))
        count += 1
        #if(not recognitionFunction == 0):
            #control = recognitionFunction()
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
        ###### regionOfInterest = extractRegionofInterest(snapshot)
        noBackground = thresholdHSVBackground(snapshot)
        displayImage(noBackground, "no bg")
        # grayscaleROI = convertToGrayscale(regionOfInterest)
        # blurROI = blurImage(grayscaleROI)
        # RECOGNITION FUNCTION GOES HERE. FEED THE getPrediction() FUNCTION WITH THE BLUR ROI IMAGE.
        # saveImage(blurROI, (FRAMES_SAVE_PATH + "frame" + str(count)))
        count += 1
        # if (not recognitionFunction == 0):
            # control = recognitionFunction()
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
        # noBackground = removeBackground(snapshot)
        # if (not recognitionFunction == 0):
            # control = recognitionFunction()
        drawBoundingRectangle(snapshot)
        displayImage(snapshot, "Original")
        k = cv2.waitKey(30) & 0xff
        if (k == 27):
            break
        if (k == captureKey):
            ###### regionOfInterest = extractRegionofInterest(snapshot)
            # grayscaleROI = convertToGrayscale(regionOfInterest)
            # blurROI = blurImage(grayscaleROI)
            noBackground = thresholdHSVBackground(snapshot)
            displayImage(noBackground, "no bg")
            # RECOGNITION FUNCTION GOES HERE. FEED THE getPrediction() FUNCTION WITH THE BLUR ROI IMAGE.
            # saveImage(blurROI, (FRAMES_SAVE_PATH + "frame" + str(count)))
            # print("Captured frame %d", (count))
            count += 1
    if (DEBUG_MODE):
        prettyPrintElapsedTime()

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
# Deprecated
def removeBackground(frame):
    # foregroundMask = BACKGROUND_MODEL.apply(frame)
    # # White rectangle
    # kernel = numpy.ones((3, 3), numpy.uint8)
    # # Convolve it with the mask
    # # Two iteration of erosion provides better results
    # foregroundMask = cv2.erode(foregroundMask, kernel, iterations=2)
    # return cv2.bitwise_and(frame, frame, mask=foregroundMask)
    pass

def getPrediction(cnnModel, image):
    processedImage = preprocessImage(image)
    predictedProbability = cnnModel.predict(processedImage)[0]
    highestPredictedWeight = max(predictedProbability)
    predictedLabel = list(predictedProbability).index(highestPredictedWeight)

    return highestPredictedWeight, predictedLabel

def getPredictedTextEquivalent(predictedLabel):
    return LABELS[int(predictedLabel)]

def preprocessImage(image):
    img = cv2.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT))
    img = numpy.array(img, dtype=numpy.float32)
    img = numpy.reshape(img, (1, IMAGE_WIDTH, IMAGE_HEIGHT, 1))

    return image

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
    # from Algorithms.CNN import CreateDataset, TrainModel
    enableCVOptimizations()
    createHSVTrackBars()
    initVideoRecording(initDevice(), 1)

# Init a silent voice project
if(__name__ == "__main__"):
    main()