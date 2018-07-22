import cv2 as cv
import Modules.CNN.RecognizeASL as asl


#vid = cv.VideoCapture("F:\School Folder\Thesis Images\Images\\7-7-2018.mp4")
vid = cv.VideoCapture(0)

# while 1:
#
#     _,img = vid.read()
asl.createHSVTrackBars()
asl.startVideoCapture(vid,enableRecording=False,enableFrameSaving=True)

    # cv.imshow("lul",img)
    #
    # k = cv.waitKey(5) & 0xFF
    # if k == 27:
    #     break