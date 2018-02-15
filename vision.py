import cv2, sys, re
from pydc1394 import Camera
import filterlib
import objectDetection
from objectDetection import Agent

#=============================================================================================
# Mouse callback Functions
#=============================================================================================
def showClickedCoordinate(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        mouseX,mouseY = x,y
        print('Clicked position  x: {} y: {}'.format(x,y))



class Vision(object):
    def __init__(self):
        self._isUpdating = True
        self._isFilterBypassed = True
        self._isObjectDetection = False
        self._detectionAlgorithm = ''
        self.frame = None # last captured frame
        self.filterRouting = [] # data structure: {"filterName", "args"}, defined in the editor
        # define the agents that you want to detect with objectDetection algorithm
        self.agent1 = Agent()
        self.agent2 = Agent()

        #=================================================
        # If using a USB webcamera
        #=================================================
        # self.cap = cv2.VideoCapture(0)
        # if not self.cap.isOpened():
        #     print('Camera is not detected. End program.')
        #     self.cap.release()
        #     sys.exit()

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

        cv2.namedWindow('Capture (Click to show coordinate)',16) # cv2.GUI_NORMAL = 16
        cv2.setMouseCallback('Capture (Click to show coordinate)',showClickedCoordinate)

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
        #     cv2.imshow('Capture (Click to show coordinate)',frameProcessed)
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
            cv2.imshow('Capture (Click to show coordinate)',frameProcessed)
            self.frame = frameProcessed
            frameOriginal.enqueue()


    #==============================================================================================
    # set instance attributes
    #==============================================================================================
    def setStateUpdate(self,state):
        self._isUpdating = state

    def setStateFiltersBypass(self,state):
        self._isFilterBypassed = state

    def setStateObjectDetection(self,state,algorithm):
        self._isObjectDetection = state
        self._detectionAlgorithm = algorithm

    #==============================================================================================
    # <Filters>
    # Define the filters in filterlib.py
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
        # You can add custom filters here if you don't want to use the editor
        return outputImage

    #==============================================================================================
    # <object detection>
    # Object detection algorithm is executed after all the filters
    # It is assumed that "imageFiltered" is used for detection purpose only;
    # the boundary of the detected object will be drawn on "imageOriginal".
    # information of detected objects can be stored in an instance of "Agent" class.
    #==============================================================================================
    def processObjectDetection(self,imageFiltered,imageOriginal):
        # convert to rgb so that coloured lines can be drawn on top
        imageOriginal = cv2.cvtColor(imageOriginal, cv2.COLOR_GRAY2RGB)

        # object detection algorithm starts here
        # In this function, information about the agent will be updated, and the original image with
        # the detected objects highlighted will be returned
        algorithm = getattr(objectDetection,self._detectionAlgorithm,objectDetection.algorithmNotDefined)
        imageProcessed = algorithm(imageFiltered,imageOriginal,self.agent1) # pass instances of Agent class if you want to update its info
        return imageProcessed
