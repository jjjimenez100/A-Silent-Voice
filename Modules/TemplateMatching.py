import cv2
import numpy as np
import OpenCVWrapper as wrap
from threading import Thread


class TemplateMatching(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.found = False
        self.started = False
        self.values = list()
        self.textValues = list()
        self.img_rgb = 0
        self.img_g = 0

    def plsrun(self):
        self.started = True

    def setVideoImage(self, rgb, g):
        self.img_rgb = rgb
        self.img_g = g

    def run(self):
        while self.started:
            frmC = 0
            templateImage = r"C:\School\thesis\Program\frames\frame" + str(frmC) + ".png"
            self.template = cv2.imread(templateImage, 0)
            self.w, self.h = self.template.shape[::-1]

            res = cv2.matchTemplate(self.img_g, self.template, cv2.TM_CCOEFF_NORMED)
            # print(res)

            th = 0.8
            loc = np.where(res >= th)
            self.values = list()
            self.textValues = list()
            self.found = False
            for pt in zip(*loc[::-1]):
                self.values = (self.img_rgb, pt, (pt[0] + self.w, pt[1] + self.h), (255, 255, 255), 2)
                self.textValues = (
                self.img_rgb, 'Detected', (pt[0] - 10, pt[1]), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2,
                cv2.LINE_AA)
                self.found = True
                break
            frmC +=1
            frmC %= 10

def main():
    tm = TemplateMatching()
    tm.daemon = True

    vid = cv2.VideoCapture(0)

    while 1:
        _,img_rgb = vid.read()
        if not _:
            print('camera not working')
        if _:
            nb = wrap.removeBackground(img_rgb)
            nb = wrap.removeBackground(nb)

            nb = wrap.convertToGrayscale(nb)
            img_g = wrap.blurImage(nb)

            tm.setVideoImage(img_rgb,img_g)

            box = list()
            text = list()

            if not tm.started:
                tm.plsrun()
                tm.start()
            if tm.found:
                box = tm.values
                text = tm.textValues
                print(text[1])
                cv2.rectangle(img_rgb,box[1],box[2],box[3],box[4])
                cv2.putText(img_rgb, text[1], text[2], text[3], text[4], text[5], text[6], text[7])
                print('detected')


            cv2.imshow('gray', img_g)
            cv2.imshow('orig', img_rgb)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    vid.release()

if __name__ == '__main__':
    main()