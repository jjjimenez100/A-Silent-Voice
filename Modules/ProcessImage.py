import cv2
import numpy
from Modules.OpenCVWrapper import createNewWindow, createTrackbar

BOX_Y = 80
BOX_X = 300
BOX_WIDTH = 300 #300
BOX_HEIGHT = 300 #300


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

def extractRegionofInterest(snapshot):
    return snapshot[BOX_Y:BOX_Y+BOX_HEIGHT,BOX_X:BOX_X+BOX_WIDTH]

def drawBoundingRectangle(snapshot):
    return cv2.rectangle(snapshot, (BOX_X, BOX_Y),
                         (BOX_X+BOX_WIDTH,BOX_Y+BOX_HEIGHT), (255,0,0),2)

def extractRegionofInterest(snapshot):
    #return snapshot[0:int(RECT_BEGIN_Y * snapshot.shape[0]),
    #          int(RECT_BEGIN_X * snapshot.shape[1]):snapshot.shape[1]]
    return snapshot[BOX_Y:BOX_Y+BOX_HEIGHT,BOX_X:BOX_X+BOX_WIDTH]
