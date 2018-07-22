import cv2
import os

class Recorder:
    def __init__(self, width, height, saveLocation="", frameName=''):
        self.dir = [os.path.dirname(saveLocation), os.path.dirname(saveLocation + "/frames/"), os.path.dirname(saveLocation + "/frames/rgb/"),
                    os.path.dirname(saveLocation + "/frames/processed/"), os.path.dirname(saveLocation + "/frames/greyscale/")]
        self.__checkSaveLocation__(self.dir)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(saveLocation+"/"+'output.mp4', fourcc, 20.0, (width, height))
        self.saveLoc = saveLocation
        self.frameName = frameName
        self.frameCountRGB = 0
        self.frameCountGREY = 0
        self.frameCountBW = 0

    def countStart(self, count):
        self.frameCountRGB = count
        self.frameCountGREY = count
        self.frameCountBW = count

    def __checkSaveLocation__(self, dir):
        for i in dir:
            print(i)
            if not os.path.exists(i):
                os.mkdir(i)

    def recordFrame(self, frame):
        self.out.write(frame)

    def saveFrame(self, frame, type='RGB'):
        frame = cv2.resize(frame, (50, 50))
        if type=='RGB':
            cv2.imwrite(self.dir[2]+"/"+self.frameName+str(self.frameCountRGB)+".png", frame)
            self.frameCountRGB +=1
        if type=='BW':
            cv2.imwrite(self.dir[3]+"/"+self.frameName+str(self.frameCountGREY)+".png", frame)
            self.frameCountGREY +=1
        if type=='GREY':
            cv2.imwrite(self.dir[4]+"/"+self.frameName+str(self.frameCountBW)+".png", frame)
            self.frameCountBW +=1

    def onDone(self):
        self.out.release()



