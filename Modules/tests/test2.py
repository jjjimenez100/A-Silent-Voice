import cv2 as cv
import Modules.CNN.RecognizeASL as asl

vid = cv.VideoCapture("F:\School Folder\Thesis Images\Images\\7-7-2018.mp4")

#while 1:

    #_,img = vid.read()
asl.createHSVTrackBars()
asl.timeBasedRecording(vid, 1)

    #cv.imshow("lul",img)

    # k = cv.waitKey(5) & 0xFF
    # if k == 27:
    #     break