import cv2, sys, re
from pydc1394 import Camera
import filterlib
import objectDetection

class Vision(object):
    def __init__(self):
        self._isUpdating = True
        self._isFilterBypassed = True
        self._isObjectDetection = False
        self.frame = None # last captured frame

        # data structure: {"filterName", "args"} defined in the editor
        self.filterRouting = []
        #=================================================
        # If using a USB webcamera
        #=================================================
        # self.cap = cv2.VideoCapture(0)
        # if not self.cap.isOpened():
        #     print('Camera is not detected. End program.')
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
        # if self._isUpdating:
        #     _, frameOriginal = self.cap.read()
        #     if not self._isFilterBypassed and not self.filterRouting == []:
        #         frameFiltered = self.processFilters(frameOriginal.copy())
        #     else:
        #         frameFiltered = frameOriginal
        #     if self._isObjectDetection:
        #         frameProcessed = self.processObjectDetection(frameFiltered,frameOriginal)
        #     else:
        #         frameProcessed = frameFiltered
        #     cv2.imshow('Realtime Capture',frameProcessed)
        #     self.frame = frameProcessed

        #=================================================
        # If using firewire camera
        #=================================================
        if self._isUpdating:
            frameOriginal = self.cam.dequeue()
            if not self._isFilterBypassed and not self.filterRouting == []:
                frameFiltered = self.processFilters(frameOriginal.copy())
            else:
                frameFiltered = frameOriginal
            if self._isObjectDetection:
                frameProcessed = self.processObjectDetection(frameFiltered,frameOriginal)
            else:
                frameProcessed = frameFiltered
            cv2.imshow('Realtime Capture',frameProcessed)
            self.frame = frameProcessed
            frameOriginal.enqueue()


    #==============================================================================================
    # set instance attributes
    #==============================================================================================
    def setStateUpdate(self,state):
        self._isUpdating = state

    def setStateFiltersBypass(self,state):
        self._isFilterBypassed = state

    def setStateObjectDetection(self,state):
        self._isObjectDetection = state

    #==============================================================================================
    # process of filters in the vision tab
    # define the filters in filterlib.py
    #==============================================================================================
    def createFilterRouting(self,text):
        self.filterRouting = []
        for line in text:
            line = line.split('//')[0]  # strip after //
            line = line.strip()         # strip spaces at both ends
            match = re.match(r"(?P<function>[a-z0-9_]+)\((?P<args>.+)\)", line)
            if match:
                name = match.group('function')
                args = match.group('args')
                args = re.sub(r'\s+', '', args) # strip spaces in args
                self.filterRouting.append({'filterName': name, 'args': args})

    def processFilters(self,image):
        for item in self.filterRouting:
            outputImage = getattr(filterlib,item['filterName'])(image,item['args'])
        '''You can add custom filters here if you don't want to use the editor'''
        return outputImage

    #==============================================================================================
    # object detection is done after all the filters
    # It is assumed that imageFiltered is used for detection purpose only;
    # the boundary of the detected object will be drawn on imageOriginal.
    # information of detected objects can be stored in the vision.<propertyName>
    # so that subthread can access it directly
    #==============================================================================================
    def processObjectDetection(self,imageFiltered,imageOriginal):
        # convert to rgb so that coloured lines can be drawn on top
        imageOriginal = cv2.cvtColor(imageOriginal, cv2.COLOR_GRAY2RGB)
        # object detection algorithm starts here
        screenCnt = objectDetection.biggestSquareContour(imageFiltered,sampleNum=5,epsilon=20)
        if not screenCnt == []:
            cv2.drawContours(imageOriginal, [screenCnt], -1, (0, 255, 0), 3)
        return imageOriginal
