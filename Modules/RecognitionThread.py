from threading import Thread
import cv2 as cv
import numpy as np


# Is a thread that classifies images into their letter counterparts
class Recoginize(Thread):
    def __init__(self, model):
        Thread.__init__(self)
        self.model = model
        self.predictedLetter = ''
        self.acc = 0
        self.img = 0

    # Image to Predict
    def predict(self, img):
        self.img = img

    # Predicted letter
    def getPrediction(self):
        return self.predictedLetter, self.acc

    def run(self):
        while True:
            if type(self.img) == type(np.ndarray(0)):
                cv.imwrite("img.jpg", cv.resize(self.img, (150, 150)))
                pred, acc = self.model.classifyImage("img.jpg")
                self.predictedLetter = pred
                self.acc = acc
            elif type(self.img) == type(""):
                print("killed", self.img)
                break
