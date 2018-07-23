from Modules.OpenCVWrapper import *
import os, time, platform
from Modules.CNN.Constants import *
from keras.models import load_model
#VideoRecorder
import Modules.tests.VideoRecorder as vr

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
CNN_MODEL = load_model(MODEL_PATH)

# Region of interest, the bounding rectangle constants
RECT_BEGIN_X = 0.25
RECT_BEGIN_Y = 0.7
BOX_Y = 80
BOX_X = 300
BOX_WIDTH = 100 #300
BOX_HEIGHT = 100 #300

#Frame snapshot counter
FRAME_SAVE_MAX = 30

# Blur value constant using KNN Gaussian
BLUR_VALUE = 41

#DIRECTORIES TO SAVE IN
MAIN_DIR = "F:\School Folder\Thesis P3\Modules/tests"

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
    startVideoCapture(device, snapshotTime)

#  Take snapshots from video recording every n seconds
def startVideoCapture(device: cv2.VideoCapture, enableRecording=False, enableFrameSaving=False):
    if enableRecording or enableFrameSaving:
        record = vr.Recorder(len(device.read()[1][1]),len(device.read()[1]), saveLocation=MAIN_DIR)
        recordStart = False

    flipped = False
    current=65
    paused = False

    if(DEBUG_MODE):
        setInitialTime()
    start = False
    recordedCount = 0
    totalCount = 0

    while(True):
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            start = True
        if start:
            isRecording, snapshot = device.read()
            if flipped:
                cv2.flip(snapshot, 1)

            if enableRecording:
                if recordStart:
                    record.recordFrame(snapshot)
                    cv2.putText(snapshot, "REC", (len(snapshot[1])-100, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2,
                                cv2.LINE_AA)
            roi = extractRegionofInterest(snapshot)
            noBackground = thresholdHSVBackground(roi)
            if enableFrameSaving:
                if recordedCount >= FRAME_SAVE_MAX:
                    print("done with",totalCount,"files",chr(current))
                    recordedCount = 0
                    recordStart = False
                    current+=1
                if recordStart:
                    recordedCount += 1
                    totalCount += 1
                    print(recordedCount)
                    record.saveFrame(roi, 'RGB', letter=current)
                    record.saveFrame(noBackground, 'BW', letter=current)
                    record.saveFrame(convertToGrayscale(roi), 'GREY', letter=current)
                    cv2.putText(snapshot, "SNAPSHOT REC ["+chr(current)+"]"+str(recordedCount/FRAME_SAVE_MAX*100), (len(snapshot[1])-430, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2,
                                cv2.LINE_AA)
                if paused and not recordStart:
                    cv2.putText(snapshot,
                                "PAUSED SNAPSHOT REC [" + chr(current) + "]" + str(recordedCount / FRAME_SAVE_MAX * 100),
                                (len(snapshot[1]) - 600, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2,
                                cv2.LINE_AA)
            displayImage(noBackground, "no bg")

            # PREDICTION FUNC
            # acc,pred = getPrediction(CNN_MODEL, noBackground)
            # word = getPredictedTextEquivalent(pred)
            # if(acc>=0.8):
            #     cv2.putText(snapshot, word + " " + str(acc), (50,50),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2,
            #         cv2.LINE_AA)

            snapshot = drawBoundingRectangle(snapshot)
            displayImage(snapshot, "Original")
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
                record.onDone()
            if enableRecording or enableFrameSaving:
                if k == ord('r'):
                    record.countStart(0)
                    recordStart = True
                    paused = False
            if recordStart:
                if k == ord('p'):
                    recordStart = False
                    paused = True
            if k == ord('b'):
                global BOX_HEIGHT, BOX_WIDTH
                BOX_HEIGHT = 300
                BOX_WIDTH = 300
    if(DEBUG_MODE):
        prettyPrintElapsedTime()


# Turns grayscale to black and white
# NOTE: dunno if it will lag
def blackWhite(img, threshold = 25):
    for i in img:
        i[i>threshold]=255
        i[i<=threshold]=0
    return img

# Draw a bounding rectangle on the image, specified by the RECT_BEGIN constants
def drawBoundingRectangle(snapshot):
    #return cv2.rectangle(snapshot, (int(RECT_BEGIN_X * snapshot.shape[1]), 0),
    #              (snapshot.shape[1], int(RECT_BEGIN_Y * snapshot.shape[0])), (255, 0, 0), 2)
    return cv2.rectangle(snapshot, (BOX_X, BOX_Y),
                         (BOX_X+BOX_WIDTH,BOX_Y+BOX_HEIGHT), (255,0,0),2)

# Extract region of interest specified by the bounding rectangle.
def extractRegionofInterest(snapshot):
    #return snapshot[0:int(RECT_BEGIN_Y * snapshot.shape[0]),
    #          int(RECT_BEGIN_X * snapshot.shape[1]):snapshot.shape[1]]
    return snapshot[BOX_Y:BOX_Y+BOX_HEIGHT,BOX_X:BOX_X+BOX_WIDTH]

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
    #displayImage(processedImage, "processed")
    predictedProbability = cnnModel.predict(processedImage)[0]
    highestPredictedWeight = max(predictedProbability)
    predictedLabel = list(predictedProbability).index(highestPredictedWeight)

    return highestPredictedWeight, predictedLabel

def getPredictedTextEquivalent(predictedLabel):
    return LABELS[int(predictedLabel)]

def preprocessImage(image):
    img = cv2.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT))
    displayImage(img, "50x50")
    img = numpy.array(img, dtype=numpy.float32)
    img = numpy.reshape(img, (1, IMAGE_WIDTH, IMAGE_HEIGHT, 1))
    return img

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