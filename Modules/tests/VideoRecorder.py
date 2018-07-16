import cv2

class Recorder:
    def __init__(self, width, height):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (width, height))

    def recordFrame(self, frame):
        self.out.write(frame)

    def onDone(self):
        self.out.release()



