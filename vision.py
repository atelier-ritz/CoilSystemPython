import cv2
import sys

class Vision(object):
    def __init__(self):
        self.isUpdating = True
        self.cap = cv2.VideoCapture(0)
        print('Camera working = {}'.format(self.cap.isOpened()))
        if not self.cap.isOpened():
            print('End program')
            self.cap.release()
            sys.exit()
        cv2.namedWindow("Realtime Capture",16) # cv2.GUI_NORMAL = 16

    def updateFrame(self):
        if self.isUpdating:
            _, frame = self.cap.read()
            grey = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
            cv2.imshow('Realtime Capture',grey)

    def setState(self,state):
        self.isUpdating = state
