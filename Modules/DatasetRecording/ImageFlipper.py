import cv2 as cv
import os


# Flips the image and saves it to the same directory
class FlipImages:
    def __init__(self, directory, startCount):
        self.dir = directory
        self.count = startCount

    # Starts the image flipping
    def start(self):
        count = self.count
        for path, dir, file in os.walk(self.dir):
            for img in file:
                cv.imwrite(path + "/" + str(count) + ".png",
                           cv.flip(cv.imread(path + "/" + img), 1))
                print("wrote in ", path + "/" + str(count) + ".png")
                count += 1
            count = self.count
