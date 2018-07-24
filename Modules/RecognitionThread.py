from threading import Thread
import cv2 as cv

class Recoginize(Thread):
    def __init__(self, model):
        Thread.__init__(self)
        self.model = model
        self.img = ''

    def predict(self, img):
        self.img = img

    def run(self):
        pass
