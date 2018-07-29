import cv2 as cv
from Modules.OpenCVWrapper import displayImage, convertToGrayscale
import Modules.DatasetRecording.VideoRecorder as vr
import Modules.ProcessImage as process


#DIRECTORIES TO SAVE IN
MAIN_DIR = "F:\School Folder\Thesis P3\Modules/tests"

#Frame snapshot counter
FRAME_SAVE_MAX = 30

vid = cv.VideoCapture("F:\School Folder\Thesis Images\Images\\7-7-2018.mp4")
process.createHSVTrackBars()
#vid = cv.VideoCapture(0)



def startVideoCapture(device: cv.VideoCapture, enableRecording=False, enableFrameSaving=False):

    record = vr.Recorder(len(device.read()[1][1]),len(device.read()[1]), saveLocation=MAIN_DIR)
    current=ord('A')
    recordedCount = 0
    totalCount = 0

    recordStart = False

    flipped = True
    paused = False


    while(True):
        k = cv.waitKey(5) & 0xFF
        isRecording, snapshot = device.read()

        if flipped:
            snapshot = cv.flip(snapshot, 1)

        if enableRecording:
            if recordStart:
                record.recordFrame(snapshot)
                cv.putText(snapshot, "REC", (len(snapshot[1])-100, 50), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2,
                            cv.LINE_AA)

        roi = process.extractRegionofInterest(snapshot)
        noBackground = process.thresholdHSVBackground(roi)
        #displayImage(noBackground, "no bg")

        #PART OF FRAME/VIDEO RECORDING
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
                cv.putText(snapshot, "SNAPSHOT REC ["+chr(current)+"]"+str(recordedCount/FRAME_SAVE_MAX*100), (len(snapshot[1])-430, 50), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2,
                            cv.LINE_AA)
            if paused and not recordStart:
                cv.putText(snapshot,
                            "PAUSED SNAPSHOT REC [" + chr(current) + "]" + str(recordedCount / FRAME_SAVE_MAX * 100),
                            (len(snapshot[1]) - 600, 50), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2,
                            cv.LINE_AA)

        snapshot = process.drawBoundingRectangle(snapshot)
        displayImage(snapshot, "Original")
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


startVideoCapture(vid,enableRecording=False,enableFrameSaving=True)