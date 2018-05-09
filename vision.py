import cv2, sys, re, time
from pydc1394 import Camera
import filterlib
import objectDetection
from objectDetection import Agent

#=============================================================================================
# Mouse callback Functions
#=============================================================================================
def showClickedCoordinate(event,x,y,flags,param):
    # global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        # mouseX,mouseY = x,y
        print('Clicked position  x: {} y: {}'.format(x,y))

class Vision(object):
    def __init__(self,index,type,guid=0000000000000000,buffersize=10):
        self._id = index
        self._type = type
        self._guid = guid
        self._isUpdating = True
        self._isFilterBypassed = True
        self._isObjectDetectionRunning = False
        self._detectionAlgorithm = ''
        self.filterRouting = [] # data structure: {"filterName", "args"}, defined in the editor
        # define the agents that you want to detect with objectDetection algorithm
        self.agent1 = Agent()
        self.agent2 = Agent()

        if self.isFireWire():
            self.cam = Camera(guid=self._guid)
            print("====================================================")
            print("CameraId:", self._id)
            print("Vendor:", self.cam.vendor)
            print("Model:", self.cam.model)
            print("GUID:", self.cam.guid)
            print("Mode:", self.cam.mode)
            print("Framerate: ", self.cam.rate)
            print("Available modes", [mode.name for mode in self.cam.modes])
            print("====================================================")
            self.cam.start_capture(bufsize=buffersize)
            self.cam.start_video()
        else:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print('Camera is not detected. End program.')
                self.cap.release()
                sys.exit()

        cv2.namedWindow(self.windowName(),16) # cv2.GUI_NORMAL = 16
        cv2.moveWindow(self.windowName(), 600,-320+340*self._id);
        cv2.setMouseCallback(self.windowName(),showClickedCoordinate)

    def updateFrame(self):
        if self.isFireWire():
            if self.isUpdating():
                frameOriginal = self.cam.dequeue()
                if not self.isFilterBypassed() and not self.filterRouting == []:
                    frameFiltered = self.processFilters(frameOriginal.copy())
                else:
                    frameFiltered = frameOriginal
                if self.isObjectDetectionRunning():
                    frameProcessed = self.processObjectDetection(frameFiltered,frameOriginal)
                else:
                    frameProcessed = frameFiltered
                cv2.imshow(self.windowName(),frameProcessed)
                frameOriginal.enqueue()
        else:
            if self.isUpdating():
                _, frameOriginal = self.cap.read()
                if not self.isFilterBypassed() and not self.filterRouting == []:
                    frameFiltered = self.processFilters(frameOriginal.copy())
                else:
                    frameFiltered = frameOriginal
                if self.isObjectDetectionRunning():
                    frameProcessed = self.processObjectDetection(frameFiltered,frameOriginal)
                else:
                    frameProcessed = frameFiltered
                cv2.imshow(self.windowName(),frameProcessed)

    #==============================================================================================
    # obtain instance attributes
    #==============================================================================================
    def windowName(self):
        return 'CamID:{} (Click to print coordinate)'.format(self._id)

    def isFireWire(self):
        return self._type.lower() == 'firewire'

    def isUpdating(self):
        return self._isUpdating

    def isFilterBypassed(self):
        return self._isFilterBypassed

    def isObjectDetectionRunning(self):
        return self._isObjectDetectionRunning

    #==============================================================================================
    # set instance attributes
    #==============================================================================================
    def setStateUpdate(self,state):
        self._isUpdating = state

    def setStateFiltersBypassed(self,state):
        self._isFilterBypassed = state

    def setStateObjectDetection(self,state,algorithm):
        self._isObjectDetectionRunning = state
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
            match = re.match(r"(?P<function>[a-z0-9_]+)\((?P<args>.*)\)", line)
            if match:
                name = match.group('function')
                args = match.group('args')
                args = re.sub(r'\s+', '', args) # strip spaces in args
                self.filterRouting.append({'filterName': name, 'args': args})

    def processFilters(self,image):
        for item in self.filterRouting:
            image = getattr(filterlib,item['filterName'],filterlib.filterNotDefined)(image,item['args'])
        # You can add custom filters here if you don't want to use the editor
        return image

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
