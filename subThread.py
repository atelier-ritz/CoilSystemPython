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
                        'default':['param0','param1','param2','param3','param4']}
        self.minOnGui = {'twistField': [-100,0,-360,0,0],
                        'rotateXY': [-100,0,0,0,0],
                        'rotateYZ': [-100,0,0,0,0],
                        'rotateXZ': [-100,0,0,0,0],
                        'default':[0,0,0,0,0]}
        self.maxOnGui = {'twistField': [100,14,360,180,360],
                        'rotateXY': [100,14,0,0,0],
                        'rotateYZ': [100,14,0,0,0],
                        'rotateXZ': [100,14,0,0,0],
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
        #=============================
        # reference params
        # 0 'Frequency (Hz)'
        # 1 'Magniude (mT)'
        # 2 'AzimuthalAngle (deg)'
        # 3 'PolarAngle (deg)'
        # 4 'SpanAngle (deg)'
        #=============================
        startTime = time.time()
        record = 'Time(s), FieldX(mT), FiledY(mT), FieldZ(mT) \n' # output to a txt file
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
            if counter > 100:
                counter = 0
                record = record + '{:.5f}, {:.2f}, {:.2f}, {:.2f}\n'.format(t,fieldX,fieldY,fieldZ)

            # print the position of the detected object
            # print('X: {}, Y: {}'.format(self.vision.agent1.x,self.vision.agent1.y))

            if self.stopped:
                text_file = open("Output.txt", "w")
                text_file.write(record)
                text_file.close()
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

    def rotateYZ(self):
        #=============================
        # reference params
        # 0 'Frequency (Hz)'
        # 1 'Magniude (mT)'
        #=============================
        startTime = time.time()
        while True:
            t = time.time() - startTime # elapsed time (sec)
            theta = 2 * pi * self.params[0] * t
            fieldY = self.params[1] * cos(theta)
            fieldZ = self.params[1] * sin(theta)
            self.field.setY(fieldY)
            self.field.setZ(fieldZ)
            if self.stopped:
                return
