import time
from mathfx import *
from math import pi, sin, cos
from PyQt5.QtCore import pyqtSignal, QMutexLocker, QMutex, QThread

def subthreadNotDefined():
    print('Subthread not defined.')
    return

class SubThread(QThread):
    statusSignal = pyqtSignal(str)

    def __init__(self,field,vision,parent=None,):
        super(SubThread, self).__init__(parent)
        self.stopped = False
        self.mutex = QMutex()
        self.field = field
        self.vision = vision

        self._subthreadName = ''
        self.params = [0,0,0,0,0]
        self.labelOnGui = {'twistField': ['Frequency (Hz)','Magniude (mT)','AzimuthalAngle (deg)','PolarAngle (deg)','SpanAngle (deg)'],
                        'rotateXY': ['Frequency (Hz)','Magniude (mT)','N/A','N/A','N/A'],
                        'rotateYZ': ['Frequency (Hz)','Magniude (mT)','N/A','N/A','N/A'],
                        'rotateXZ': ['Frequency (Hz)','Magniude (mT)','N/A','N/A','N/A'],
                        'cutting_oni': ['Frequency (Hz)','Magniude (mT)','N/A','N/A','N/A'],
                        'default':['param0','param1','param2','param3','param4']}
        self.defaultValOnGui = {
                        'twistField': [0,0,0,0,0],
                        'default':[0,0,0,0,0]
                        }
        self.minOnGui = {'twistField': [-100,0,-1080,0,0],
                        'rotateXY': [-100,0,0,0,0],
                        'rotateYZ': [-100,0,0,0,0],
                        'rotateXZ': [-100,0,0,0,0],
                        'cutting_oni': [-30,-14,0,0,0],
                        'default':[0,0,0,0,0]}
        self.maxOnGui = {'twistField': [100,14,1080,180,360],
                        'rotateXY': [100,14,0,0,0],
                        'rotateYZ': [100,14,0,0,0],
                        'rotateXZ': [100,14,0,0,0],
                        'cutting_oni': [30,14,0,0,0],
                        'default':[0,0,0,0,0]}

    def setup(self,subThreadName):
        self._subthreadName = subThreadName
        self.stopped = False

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stopped = True

    def run(self):
        subthreadFunction = getattr(self,self._subthreadName,subthreadNotDefined)
        subthreadFunction()
        # self.stop()
        # self.finished.emit()

    def setParam0(self,val): self.params[0] = val
    def setParam1(self,val): self.params[1] = val
    def setParam2(self,val): self.params[2] = val
    def setParam3(self,val): self.params[3] = val
    def setParam4(self,val): self.params[4] = val

    #=========================================
    # Start defining your subthread from here
    #=========================================
    def twistField(self):
        #======================d=======
        # reference params
        # 0 'Frequency (Hz)'
        # 1 'Magniude (mT)'
        # 2 'AzimuthalAngle (deg)'
        # 3 'PolarAngle (deg)'
        # 4 'SpanAngle (deg)'
        #=============================
        startTime = time.time()
        record = 'Time(s), FieldX(mT), FiledY(mT), FieldZ(mT), X(pixel), Y(pixel) \n' # output to a txt file
        counter = 0
        while True:
            t = time.time() - startTime # elapsed time (sec)
            fieldX = self.params[1]* ( cosd(self.params[2])*cosd(self.params[3])*cosd(90-self.params[4]*0.5)*cos(2*pi*self.params[0]*t) - sind(self.params[2])*cosd(90-self.params[4]*0.5)*sin(2*pi*self.params[0]*t) + cosd(self.params[2])*sind(self.params[3])*cosd(self.params[4]*0.5));
            fieldY = self.params[1]* ( sind(self.params[2])*cosd(self.params[3])*cosd(90-self.params[4]*0.5)*cos(2*pi*self.params[0]*t) + cosd(self.params[2])*cosd(90-self.params[4]*0.5)*sin(2*pi*self.params[0]*t) + sind(self.params[2])*sind(self.params[3])*cosd(self.params[4]*0.5));
            fieldZ = self.params[1]* (-sind(self.params[3])*cosd(90-self.params[4]*0.5)*cos(2*pi*self.params[0]*t) + cosd(self.params[3])*cosd(self.params[4]*0.5));
            self.field.setX(fieldX)
            self.field.setY(fieldY)
            self.field.setZ(fieldZ)
            # save to txt
            counter += 1
            if counter > 300:
                counter = 0
                record = record + '{:.5f}, {:.2f}, {:.2f}, {:.2f}, {}, {}\n'.format(t,self.field.x,self.field.y,self.field.z,self.vision.agent1.x,self.vision.agent1.y)
            if self.stopped:
                text_file = open("Output.txt", "w")
                text_file.write(record)
                text_file.close()
                return

    def exampleOscBetween(self):
        """ 
        oscBetween() defined in mathfx returns a value that oscillates between the lower and upper bounds.
        oscBetween(currentTime,oscShape,frequency,lowerBound,upperBound,phaseOffset(optional)) 
        oscShape = 'saw','triangle','square','sin' '''
        It returns the "lowerBound" when currentTime = 0
        """
        startTime = time.time()
        while True:
            t = time.time() - startTime # elapsed time (sec)
            
            # Example 1: oscillate between -10 mT to 10 mT in X
            fieldX = oscBetween(t,'triangle',params[0],-10,10)
            self.field.setX(fieldX)
            
            # Example 2: apply a 10 mT field, switching between 0 deg and 30 deg in XY plane
            magitude = 10
            angle = oscBetween(t,'square',params[0],0,30)
            fieldX = magnitude * cosd(angle)
            fieldY = magnitude * sind(angle)
            self.field.setX(fieldX)
            self.field.setY(fieldY)

            # Example 3: apply a 10 mT field, angle in XY plane = 0,1,2,...29,30,0,1,2,...
            magitude = 10
            angle = oscBetween(t,'saw',params[0],0,30)
            fieldX = magnitude * cosd(angle)
            fieldY = magnitude * sind(angle)
            
            self.field.setX(fieldX)
            self.field.setY(fieldY)
            self.field.setZ(fieldZ)
            if self.stopped:
                return


    def rotateXY(self):
        #=============================
        # reference params
        # 0 'Frequency (Hz)'
        # 1 'Magniude (mT)'
        #=============================
        startTime = time.time()
        while True:
            t = time.time() - startTime # elapsed time (sec)
            theta = 2 * pi * self.params[0] * t
            fieldX = self.params[1] * cos(theta)
            fieldY = self.params[1] * sin(theta)
            self.field.setX(fieldX)
            self.field.setY(fieldY)
            if self.stopped:
                return

    def rotateXZ(self):
        #=============================
        # reference params
        # 0 'Frequency (Hz)'
        # 1 'Magniude (mT)'
        #=============================
        startTime = time.time()
        while True:
            t = time.time() - startTime # elapsed time (sec)
            theta = 2 * pi * self.params[0] * t
            fieldX = self.params[1] * cos(theta)
            fieldZ = self.params[1] * sin(theta)
            self.field.setX(fieldX)
            self.field.setZ(fieldZ)
            if self.stopped:
                return

    def cutting_oni(self):
        #=============================
        # reference params
        # 0 'Frequency (Hz)'
        # 1 'Magniude (mT)'
        #=============================
        startTime = time.time()
        while True:
            t = time.time() - startTime # elapsed time (sec)
            theta = 2 * pi * self.params[0] * t
            fieldZ = self.params[1] * abs(sin(theta))
            self.field.setZ(fieldZ)
            if self.stopped:
                return
