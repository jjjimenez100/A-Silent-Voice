from Modules.OpenCVWrapper import *
import os, time, platform
from Modules.CNN.Constants import *
# from keras.models import load_model
from Modules.CNN.TFModel import TFModel
# VideoRecorder
import Modules.RecognitionThread as rt
import Modules.ProcessImage as process
import Modules.WordBuilder as wb

# Constants

# FPS of video capturing device
FRAME_RATE = 7
OPERATING_SYSTEM = platform.system()
# Get the current working directory of the python file
PATH = os.path.dirname(os.path.realpath(__file__))
PREVIOUS_TIME = 0
# Enable or disable printing of texts on console to help with debugging
DEBUG_MODE = True

## Deprecated
# BACKGROUND_MODEL = createKNNBackgroundSubtractor(5000, 20)

# Uncomment for neural net
# CNN_MODEL = load_model(MODEL_PATH)

# Blur value constant using KNN Gaussian
BLUR_VALUE = 41


# Recognition class that creates the thread for recognizing images
class Recognition:
    def __init__(self):
        model = TFModel("output_graph.pb", "output_labels.txt", "Placeholder", "final_result")
        self.thread = rt.Recoginize(model)
        self.thread.daemon = True
        self.thread.start()

    # Gets an inputted images and returns the predicted letter and accuracy of the image
    def predict(self, image):
        self.thread.predict(image)
        return self.thread.getPrediction()


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
def startVideoCapture(device: cv2.VideoCapture):
    model = TFModel("output_graph.pb", "output_labels.txt", "Placeholder", "final_result")
    thread = rt.Recoginize(model)
    thread.daemon = True
    thread.start()

    builder = wb.WordBuilder()

    flipped = True

    if (DEBUG_MODE):
        setInitialTime()

    while (True):
        isRecording, snapshot = device.read()

        if flipped:
            snapshot = cv2.flip(snapshot, 1)

        roi = process.extractRegionofInterest(snapshot)
        thread.predict(roi)

        # PREDICTION
        pred, acc = thread.getPrediction()
        word = builder.checkLetter(pred)
        cv2.putText(snapshot, pred + " " + str(acc), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2,
                    cv2.LINE_AA)
        cv2.putText(snapshot, word, (50, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2,
                    cv2.LINE_AA)

        snapshot = process.drawBoundingRectangle(snapshot)
        displayImage(snapshot, "Original")
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
            record.onDone()
    if (DEBUG_MODE):
        prettyPrintElapsedTime()


# Turns grayscale to black and white
# NOTE: dunno if it will lag
def blackWhite(img, threshold=25):
    for i in img:
        i[i > threshold] = 255
        i[i <= threshold] = 0
    return img


# Try to smooth the given image by blurring it out
def blurImage(regionOfInterest):
    return cv2.GaussianBlur(regionOfInterest, (BLUR_VALUE, BLUR_VALUE), 0)


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
    displayImage(img, "50x50")
    img = numpy.array(img, dtype=numpy.float32)
    img = numpy.reshape(img, (1, IMAGE_WIDTH, IMAGE_HEIGHT, 1))
    return img


# Get current system time
def getTime():
    if (OPERATING_SYSTEM == "Windows"):
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
    initVideoRecording(initDevice(), 1)


# Init a silent voice project
if (__name__ == "__main__"):
    main()
