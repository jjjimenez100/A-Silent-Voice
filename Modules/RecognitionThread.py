from threading import Thread
import cv2 as cv
import numpy as np
import sys, queue
class Recoginize(Thread):
    def __init__(self, model, queue=queue.Queue):
        Thread.__init__(self)
        self.model = model
        self.predictedLetter = ''
        self.acc = 0
        self.img = ''
        self.queue = queue


    def predict(self, img):
        self.img = img

    def getPrediction(self):
        return self.predictedLetter, self.acc

    def run(self):
        while True:
            self.img = self.queue.get()
            if type(self.img) == type(np.ndarray(0)):
                print("walao")
                cv.imwrite("img.jpg", cv.resize(self.img, (150,150)))
                pred,acc = self.model.classifyImage("img.jpg")
                self.predictedLetter = pred
                self.acc = acc
                self.img = ''
                self.queue.task_done()
            if self.img == "kill":
                break