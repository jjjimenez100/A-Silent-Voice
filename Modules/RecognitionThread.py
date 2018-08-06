from threading import Thread
import cv2 as cv
import numpy as np
import sys
class Recoginize(Thread):
    def __init__(self, model):
        Thread.__init__(self)
        self.model = model
        self.predictedLetter = ''
        self.acc = 0
        self.img = ''

    def predict(self, img):
        self.img = img

    def getPrediction(self):
        return self.predictedLetter, self.acc

    def run(self):
        while True:
            if type(self.img) == type(np.ndarray(0)):
                cv.imwrite("img.jpg", cv.resize(self.img, (150,150)))
                pred,acc = self.model.classifyImage("img.jpg")
                self.predictedLetter = pred
                self.acc = acc
                self.img = ''


