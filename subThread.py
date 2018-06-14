import time
from mathfx import *
from math import pi, sin, cos, sqrt, atan2, degrees
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
                        'ellipse': ['Frequency (Hz)','Azimuthal Angle (deg)','B_horzF (mT)','B_vert (mT)','B_horzB (mT)'],
                        'drawing': ['pattern ID','offsetX','offsetY','N/A','N/A'],
                        'swimmerPathFollowing': ['Frequency (Hz)','Magniude (mT)','N/A','N/A','N/A'],
                        'default':['param0','param1','param2','param3','param4']}
        self.defaultValOnGui = {
                        'twistField': [0,0,0,0,0],
                        'drawing': [0,0,0,1,0],
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
                        'ellipse': [-100,-720,0,0,0],
                        'examplePiecewiseFunction': [-20,0,-360,0,0],
                        'swimmerPathFollowing': [-100,0,0,0,0],
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
                        'drawing':[2,1000,1000,10,0],
                        'swimmerPathFollowing': [100,20,0,0,0],
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

    def setParam0(self,val): self.params[0] = val
    def setParam1(self,val): self.params[1] = val
    def setParam2(self,val): self.params[2] = val
    def setParam3(self,val): self.params[3] = val
    def setParam4(self,val): self.params[4] = val

    #=========================================
    # Start defining your subthread from here
    #=========================================
    def drawing(self):
        """
        An example of drawing lines and circles in a subThread
        (Not in object detection)
        """
        #=============================
        # reference params
        # 0 'Path ID'
        # 1 'offsetX'
        # 2 'offsetY'
        # 3 'scale'
        #=============================
        startTime = time.time()
        while True:
            self.vision.clearDrawingRouting() # if we don't run this in a while loop, it freezes!!! (because *addDrawing* keeps adding new commands)
            self.vision.addDrawing('pathUT', self.params)
            self.vision.addDrawing('circle',[420,330,55])
            self.vision.addDrawing('arrow',[0,0,325,325])
            # you can also do somthing like:
            # drawing an arrow from "the robot" to "the destination point"
            t = time.time() - startTime # elapsed time (sec)
            self.field.setX(0)
            self.field.setY(0)
            self.field.setZ(0)
            if self.stopped:
                return

    def swimmerPathFollowing(self):
        '''
        An example of autonomous path following of a sinusoidal swimmer at air-water interfaceself.
        This example demonstrates the use of:
        1 - a subthread that comprises several tasks
        2 - drawing the path, target, etc. on the screen
        3 - changeing the drawings based on the current state
        '''
        #=============================
        # reference params
        # 0 'Frequency (Hz)'
        # 1 'Magnitude (mT)'
        #=============================
        startTime = time.time()
        state = 0 # indicates which goal point the robot is approaching. e.g. state0 -> approaching goalsX[0], goalsY[0]
        rect = [640,480] # size of the image. Format: width, height.
        pointsX = [0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.2] # normalized position [0,1]
        pointsY = [0.8,0.2,0.2,0.8,0.2,0.2,0.8,0.8] # normalized position [0,1]
        goalsX = [int(rect[0]* i) for i in pointsX] # actual position (pixel)
        goalsY = [int(rect[1]* i) for i in pointsY] # actual position (pixel)
        tolerance = 10 # It is considered that the robot has reached the point once the distance is less than *tolerance*
        while True:
            # obtain positions
            x = self.vision.agent1.x
            y = self.vision.agent1.y
            goalX = goalsX[state] # must be int
            goalY = goalsY[state] # must be int

            # draw reference lines
            self.vision.clearDrawingRouting() # if we don't run this in a while loop, it freezes!!! (because *addDrawing* keeps adding new commands)
            self.vision.addDrawing('closedPath',[goalsX,goalsY])
            self.vision.addDrawing('circle',[goalX,goalY,5])
            self.vision.addDrawing('line',[x,y,goalX,goalY])

            # calculate distance and angle
            distance = sqrt((goalX - x)**2 + (goalY - y)**2)
            angle = degrees(atan2(-(goalY-y),goalX-x))   # computers take top left point as (0,0)

            # check if it has reached the goal point
            if distance <= tolerance:
                state += 1
                print('>>> Step to state {} <<<'.format(state))

            # apply magnetic field
            t = time.time() - startTime # elapsed time (sec)
            theta = 2 * pi * self.params[0] * t
            fieldX = self.params[1] * cos(theta) * cosd(angle)
            fieldY = self.params[1] * cos(theta) * sind(angle)
            fieldZ = self.params[1] * sin(theta)
            self.field.setX(fieldX)
            self.field.setY(fieldY)
            self.field.setZ(fieldZ)
            if self.stopped or state == len(pointsX):
                return

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
        # 2 'B_horzF (mT)'
        # 3 'B_vert (mT)'
        # 4 'B_horzB (mT)'
        #=============================
        startTime = time.time()
        counter = 0
        record = ''
        while True:
            t = time.time() - startTime # elapsed time (sec)
            theta = 2 * pi * self.params[0] * t
            normT = normalizeTime(t,self.params[0]) # 0 <= normT < 1
            if normT < 0.5:
                B_horz = self.params[2] * cos(theta)
            else:
                B_horz = self.params[4] * cos(theta)
            fieldX = B_horz * cosd(self.params[1])
            fieldY = B_horz * sind(self.params[1])
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
