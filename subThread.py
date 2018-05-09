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
                        'osc_saw': ['Frequency (Hz)','bound1 (mT)','bound2 (mT)','Azimuth [0,360] (deg)','Polar [-90,90] (deg)'],
                        'osc_triangle': ['Frequency (Hz)','bound1 (mT)','bound2 (mT)','Azimuth [0,360] (deg)','Polar [-90,90] (deg)'],
                        'osc_square': ['Frequency (Hz)','bound1 (mT)','bound2 (mT)','Azimuth [0,360] (deg)','Polar [-90,90] (deg)'],
                        'osc_sin': ['Frequency (Hz)','bound1 (mT)','bound2 (mT)','Azimuth [0,360] (deg)','Polar [-90,90] (deg)'],
                        'oni_cutting': ['Frequency (Hz)','Magnitude (mT)','angleBound1 (deg)','angleBound2 (deg)','N/A'],
                        'examplePiecewiseFunction': ['Frequency (Hz)','Magnitude (mT)','angle (deg)','period1 (0-1)','period2 (0-1)'],
                        'ellipse': ['Frequency (Hz)','Azimuthal Angle (deg)','B_horz (mT)','B_vert (mT)','B_side (mT)'],
                        'default':['param0','param1','param2','param3','param4']}
        self.defaultValOnGui = {
                        'twistField': [0,0,0,0,0],
                        'default':[0,0,0,0,0]
                        }
        self.minOnGui = {'twistField': [-100,0,-1080,0,0],
                        'rotateXY': [-100,0,0,0,0],
                        'rotateYZ': [-100,0,0,0,0],
                        'rotateXZ': [-100,0,0,0,0],
                        'osc_saw': [-100,-20,-20,0,-90],
                        'osc_triangle': [-100,-20,-20,0,-90],
                        'osc_square': [-100,-20,-20,0,-90],
                        'osc_sin': [-100,-20,-20,0,-90],
                        'oni_cutting': [-100,-14,-720,-720,0],
                        'ellipse': [-100,-720,0,0,-20],
                        'examplePiecewiseFunction': [-20,0,-360,0,0],
                        'default':[0,0,0,0,0]}
        self.maxOnGui = {'twistField': [100,14,1080,180,360],
                        'rotateXY': [100,14,0,0,0],
                        'rotateYZ': [100,14,0,0,0],
                        'rotateXZ': [100,14,0,0,0],
                        'osc_saw': [100,20,20,360,90],
                        'osc_triangle': [100,20,20,360,90],
                        'osc_square': [100,20,20,360,90],
                        'osc_sin': [100,20,20,360,90],
                        'oni_cutting': [100,14,720,720,0],
                        'ellipse': [100,720,20,20,20],
                        'examplePiecewiseFunction': [20,20,360,1,1],
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
        # self.finished.emit()time rati

    def setParam0(self,val): self.params[0] = val
    def setParam1(self,val): self.params[1] = val
    def setParam2(self,val): self.params[2] = val
    def setParam3(self,val): self.params[3] = val
    def setParam4(self,val): self.params[4] = val

    #=========================================
    # Start defining your subthread from here
    #=========================================
    def examplePiecewiseFunction(self):
        """
        This function shows an example of a poscX_sawiecewise function.
        """
        #=============================
        # reference params
        # 0 'Frequency (Hz)'
        # 1 'Magnitude (mT)'
        # 2 'angle (deg)'
        # 3 'period1 (0-1)'
        # 4 'period2 (0-1)'
        #=============================
        startTime = time.time()

        while True:
            t = time.time() - startTime # elapsed time (sec)
            normT = normalizeTime(t,self.params[0]) # 0 <= normT < 1
            if normT < self.params[3]:
                magnitude = self.params[1] / oscX_sawself.params[3] * normT
                angle = 180
            elif normT < self.params[4]:
                magnitude = self.params[1]
                angle = (180 - self.params[2])/(self.params[3] - self.params[4]) * (normT - self.params[3]) + 180
            else:
                magnitude = self.params[1] / (self.params[4] - 1) * (normT - 1)
                angle = self.params[2]
            fieldX = magnitude * sind(angle)
            fieldY = 0
            fieldZ = magnitude * cosd(angle)
            self.field.setX(fieldX)
            self.field.setY(fieldY)
            self.field.setZ(fieldZ)
            if self.stopped:
                return

    def ellipse(self):
        #=============================
        # reference params
        # 0 'Frequency (Hz)'
        # 1 'azimuth (deg)'
        # 2 'B_horz (mT)'
        # 3 'B_vert (mT)'
        # 4 'B_side (mT)'
        #=============================
        startTime = time.time()
        counter = 0
        record = ''
        while True:
            t = time.time() - startTime # elapsed time (sec)
            theta = 2 * pi * self.params[0] * t
            B_horz = self.params[2] * cos(theta)
            fieldX = B_horz * cosd(self.params[1]) + self.params[4]*sind(self.params[1])
            fieldY = B_horz * sind(self.params[1]) - self.params[4]*cosd(self.params[1])
            fieldZ = self.params[3] * sin(theta)
            self.field.setX(fieldX)
            self.field.setY(fieldY)
            self.field.setZ(fieldZ)
            # save to txt
            counter += 1
            if counter > 10:
                counter = 0
                record = record + '{:.5f}, {:.2f}, {:.2f}, {:.2f}, {}, {}\n'.format(t,self.field.x,self.field.y,self.field.z,self.vision.agent1.x,self.vision.agent1.y)
            if self.stopped:
                text_file = open("Output.txt", "w")
                text_file.write(record)
                text_file.close()
                return

    def oni_cutting(self):
        #=============================
        # reference params
        # 0 'Frequency (Hz)'
        # 1 'Magnitude (mT)'
        # 2 'angleBound1 (deg)'
        # 3 'angleBound2 (deg)'
        #=============================
        startTime = time.time()
        while True:
            t = time.time() - startTime # elapsed time (sec)
            angle = oscBetween(t,'sin',self.params[0],self.params[2],self.params[3])
            fieldX = self.params[1] * cosd(angle)
            fieldY = self.params[1] * sind(angle)
            self.field.setX(fieldX)
            self.field.setY(fieldY)
            self.field.setZ(0)
            if self.stopped:
                return

    def twistField(self):
        ''' credit to Omid '''
        #=============================
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

    def osc_saw(self):
        #=============================
        # reference params
        # 0 'Frequency (Hz)'
        # 1 'Lowerbound (mT)'
        # 2 'Upperbound (mT)'
        # 3 'Azimuthal Angle (deg)'
        # 4 'Polar Angle (deg)'
        #=============================
        startTime = time.time()
        while True:
            t = time.time() - startTime # elapsed time (sec)
            magnitude = oscBetween(t,'saw',self.params[0],self.params[1],self.params[2])
            fieldZ = magnitude * sind(self.params[4])
            fieldX = magnitude * cosd(self.params[4]) * cosd(self.params[3])
            fieldY = magnitude * cosd(self.params[4]) * sind(self.params[3])
            self.field.setX(fieldX)
            self.field.setY(fieldY)
            self.field.setZ(fieldZ)
            if self.stopped:
                return

    def osc_triangle(self):
        #=============================
        # reference params(200,255)
        # 0 'Frequency (Hz)'
        # 1 'Lowerbound (mT)'
        # 2 'Upperbound (mT)'
        # 3 'Azimuthal Angle (deg)'
        # 4 'Polar Angle (deg)'
        #=============================
        startTime = time.time()
        while True:
            t = time.time() - startTime # elapsed time (sec)
            magnitude = oscBetween(t,'triangle',self.params[0],self.params[1],self.params[2])
            fieldZ = magnitude * sind(self.params[4])
            fieldX = magnitude * cosd(self.params[4]) * cosd(self.params[3])
            fieldY = magnitude * cosd(self.params[4]) * sind(self.params[3])
            self.field.setX(fieldX)
            self.field.setY(fieldY)
            self.field.setZ(fieldZ)
            if self.stopped:
                return

    def osc_square(self):
        #=============================
        # reference params
        # 0 'Frequency (Hz)'
        # 1 'Lowerbound (mT)'
        # 2 'Upperbound (mT)'
        # 3 'Azimuthal Angle (deg)'
        # 4 'Polar Angle (deg)'
        #=============================
        startTime = time.time()
        while True:
            t = time.time() - startTime # elapsed time (sec)
            magnitude = oscBetween(t,'square',self.params[0],self.params[1],self.params[2])
            fieldZ = magnitude * sind(self.params[4])
            fieldX = magnitude * cosd(self.params[4]) * cosd(self.params[3])
            fieldY = magnitude * cosd(self.params[4]) * sind(self.params[3])
            self.field.setX(fieldX)
            self.field.setY(fieldY)
            self.field.setZ(fieldZ)
            if self.stopped:
                return

    def osc_sin(self):
        #=============================
        # reference params
        # 0 'Frequency (Hz)'
        # 1 'Lowerbound (mT)'
        # 2 'Upperbound (mT)'
        # 3 'Azimuthal Angle (deg)'
        # 4 'Polar Angle (deg)'
        #=============================
        startTime = time.time()
        while True:
            t = time.time() - startTime # elapsed time (sec)
            magnitude = oscBetween(t,'sin',self.params[0],self.params[1],self.params[2])
            fieldZ = magnitude * sind(self.params[4])
            fieldX = magnitude * cosd(self.params[4]) * cosd(self.params[3])
            fieldY = magnitude * cosd(self.params[4]) * sind(self.params[3])
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
            self.field.setZ(0)
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
            self.field.setX(0)
            self.field.setY(fieldY)
            self.field.setZ(fieldZ)
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
            self.field.setY(0)
            self.field.setZ(fieldZ)
            if self.stopped:
                return
