import cv2
import sys
from pydc1394 import Camera
from PIL import Image
import numpy as np

class Vision(object):
    def __init__(self):
        self.isUpdating = True
        #=================================================
        # If using a USB webcamera
        #=================================================
        # self.cap = cv2.VideoCapture(0)
        # print('Camera working = {}'.format(self.cap.isOpened()))
        # if not self.cap.isOpened():
        #     print('End program')
        #     self.cap.release()
        #     sys.exit()
        # cv2.namedWindow("Realtime Capture",16) # cv2.GUI_NORMAL = 16

        #=================================================
        # If using firewire camera
        #=================================================
        # self.cam = Camera(guid=2672909587849792)
        self.cam = Camera(guid=2672909588927744)
        print("====================================================")
        print("Vendor:", self.cam.vendor)
        print("Model:", self.cam.model)
        print("GUID:", self.cam.guid)
        print("Mode:", self.cam.mode)
        print("Framerate: ", self.cam.rate)
        print("Available modes", [mode.name for mode in self.cam.modes])
        print("====================================================")
        self.cam.start_capture()
        self.cam.start_video()
        cv2.namedWindow("Realtime Capture",16) # cv2.GUI_NORMAL = 16

    def updateFrame(self):
        #=================================================
        # If using a USB webcamera
        #=================================================
        # if self.isUpdating:
        #     _, frame = self.cap.read()
        #     grey = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
        #     cv2.imshow('Realtime Capture',grey)

        #=================================================
        # If using firewire camera
        #=================================================
        if self.isUpdating:
            frame = self.cam.dequeue()
            cv2.imshow('Realtime Capture',frame)
            frame.enqueue()


    def setState(self,state):
        self.isUpdating = state
