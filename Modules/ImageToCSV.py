import cv2 as cv
import OpenCVWrapper as w
import pandas as pd
import os


class ImageToCSV:
    letters = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7
        , "I": 8, "J": 9, "K": 10, "L": 11, "M": 12, "N": 13
        , "O": 14, "P": 15, "Q": 16, "R": 17, "S": 18, "T": 19
        , "U": 20, "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25}

    @staticmethod
    def convertToCSV(path: str):
        file = list()
        count = 0

        for i in ImageToCSV.letters:
            for p, d, f in os.walk(path + "/" + str(ImageToCSV.letters[i])):
                for image in f:
                    img = cv.imread(os.path.join(p, image))
                    img = cv.resize(img,(50,50),interpolation=cv.INTER_AREA)

                    arr, c = ImageToCSV.getPixelArray(ImageToCSV.letters[i], img)
                    if c > count:
                        count = c
                    file.append(arr)



        first = ["label"]
        for i in range(count - 1):
            first.append("pixel" + str(i + 1))

        tcsv = pd.DataFrame(file)
        path += "/Template.csv"
        tcsv.to_csv(path, index=False, header=first)

    @staticmethod
    def getPixelArray(letter: int, image):
        pixels = [letter]
        image = w.convertToGrayscale(image)
        for i in image:
            for j in i:
                pixels.append(j)
        return pixels, len(pixels)