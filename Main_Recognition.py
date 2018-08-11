from Modules.CNN.RecognizeASL import *
import cv2
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

# vid = cv2.VideoCapture("F:\School Folder\Thesis Images\Images\\7-7-2018.mp4")
vid = cv2.VideoCapture(0)

startVideoCapture(vid)