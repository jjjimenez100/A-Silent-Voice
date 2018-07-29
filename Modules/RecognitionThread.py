from threading import Thread
import cv2 as cv
import sys

class Recoginize(Thread):
    def __init__(self, model):
        Thread.__init__(self)
        self.model = model
        self.img = ''
        self.predictedLetter = ''
        self.acc = 0

    def predict(self, img):
        self.img = img

    def getPrediction(self):
        return self.predictedLetter, self.acc

    def run(self):
        while True:
            if not self.img == '':
                cv.imwrite("img.jpg", cv.resize(self.img, (150,150)))
                pred,acc = self.model.predict("img.jpg")
                print(pred,acc, flush=True)
                self.predictedLetter = pred
                self.acc = acc
                self.img = ''

