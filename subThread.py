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
                        'swimmerPathFollowing': ['Frequency (Hz)','Magniude (mT)','temp angle','N/A','N/A'],
                        'default':['param0','param1','param2','param3','param4']}
        self.defaultValOnGui = {
                        'twistField': [0,0,0,0,0],
                        'drawing': [0,0,0,1,0],
                        'swimmerPathFollowing': [-20,2,0,0,0],
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
                        'swimmerPathFollowing': [100,20,360,0,0],
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
        # video writing feature
        self.vision.createVideoWriter('drawpath.avi')
        self.vision.setVideoWritingEnabled(True)
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
                self.vision.setVideoWritingEnabled(False)
                return

    def swimmerPathFollowing(self):
        '''
        An example of autonomous path following of a sinusoidal swimmer at air-water interfaceself.
        This example follows the path "M".
        '''
        #=============================
        # reference params
        # 0 'Frequency (Hz)'
        # 1 'Magnitude (mT)'
        # 3 'temp angle'
        #=============================
        startTime = time.time()
        state = 0 # indicates which goal point the robot is approaching. e.g. state0 -> approaching goalsX[0], goalsY[0]
        rect = [640,480] # size of the image. Format: width, height.
        pointsX = [0.2,0.3,0.4,0.5,0.6,0.7,0.8] # normalized position [0,1]
        pointsY = [0.7,0.3,0.3,0.7,0.3,0.3,0.7] # normalized position [0,1]
        goalsX = [int(rect[0]* i) for i in pointsX] # actual position (pixel)
        goalsY = [int(rect[1]* i) for i in pointsY] # actual position (pixel)
        tolerance = 10
        # It is considered that the robot has reached the point once the distance is less than *tolerance*
        toleranceDeviation = 30
        # Path correction is necessary when deviation exceeds this value.
        magnitudeCorrection = 1
        # Slow down the speed of the robot t oavoid overshoot when it is close to goal points
        while True:
            # obtain positions
            x = self.vision.agent1.x # curent position of the robot
            y = self.vision.agent1.y
            goalX = goalsX[state] # must be int
            goalY = goalsY[state] # must be int
            goalXPrevious = goalsX[state-1] # must be int
            goalYPrevious = goalsY[state-1] # must be int

            # draw reference lines
            self.vision.clearDrawingRouting() # if we don't run this in a while loop, it freezes!!! (because *addDrawing* keeps adding new commands)
            self.vision.addDrawing('closedPath',[goalsX,goalsY])
            self.vision.addDrawing('circle',[goalX,goalY,5])
            self.vision.addDrawing('line',[x,y,goalX,goalY])

            #=======================================================
            # calculate the heading angle
            #=======================================================
            distance = distanceBetweenPoints(x,y,goalX,goalY)
            footX, footY = perpendicularFootToLine(x,y,goalXPrevious,goalYPrevious,goalX,goalY)
            deviation = distanceBetweenPoints(x,y,footX,footY)
            if deviation > toleranceDeviation:
                # moving perpendicular to the line
                angle = degrees(atan2(-(footY-y),footX-x))
            else:
                angleRobotToGoal = atan2(-(goalY-y),goalX-x)
                angleRobotToFoot = atan2(-(footY-y),footX-x)
                angleCorrectionOffset = normalizeAngle(angleRobotToFoot - angleRobotToGoal) * deviation / toleranceDeviation
                angle = degrees(angleRobotToGoal + angleCorrectionOffset)
                # print(angleRobotToGoal,angle)

            if distance <= tolerance * 3:
                magnitudeCorrection = 0.5
            else:
                magnitudeCorrection = 1
            # check if it has reached the goal point
            if distance <= tolerance:
                state += 1
                print('>>> Step to point {} <<<'.format(state))


            # apply magnetic field
            t = time.time() - startTime # elapsed time (sec)
            theta = 2 * pi * self.params[0] * t
            fieldX = magnitudeCorrection * self.params[1] * cos(theta) * cosd(angle+self.params[2])
            fieldY = magnitudeCorrection * self.params[1] * cos(theta) * sind(angle+self.params[2])
            fieldZ = magnitudeCorrection * self.params[1] * sin(theta)
            self.field.setX(fieldX)
            self.field.setY(fieldY)
            self.field.setZ(fieldZ)
            if self.stopped or state == len(pointsX):
                return

    def swimmerBenchmark(self):
        '''
        An example of testing the velocity of the swimmer with respect to frequency and magnitude.
        It demonstrates:
            - path following: Point0 -> Point1 -> Point0
            - do the same path following task for different frequencies. (Benchmarking *velocity* vs *frequency*)
            - draw lines and circles on the frame in real time

        '''
        startTime = time.time()
        state = 0 # indicates which goal point the robot is approaching. e.g. state0 -> approaching goalsX[0], goalsY[0]
        freq = [-15,-15,-17.5,-20,-22.5,-25,-27.5,-30] # the first frequency is the freq that the robot is heading to the start point.
        magnitude = 3
        benchmarkState = 0 # indicates which frequency the program is testing

        rect = [640,480] # size of the image. Format: width, height.
        pointsX = [0.2,0.8] # normalized position [0,1]
        pointsY = [0.2,0.8] # normalized position [0,1]
        goalsX = [int(rect[0]* i) for i in pointsX] # actual position (pixel)
        goalsY = [int(rect[1]* i) for i in pointsY] # actual position (pixel)
        tolerance = 10 # It is considered that the robot has reached the point once the distance is less than *tolerance*
        print('Moving to the home position. Frequency {} Hz'.format(freq[benchmarkState]))
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
                # if at the starting point, start a new round of benchmark test
                if state == 0:
                    benchmarkState += 1
                    if benchmarkState < len(freq):
                        print('Case {} - Benchmark Frequency {} Hz'.format(benchmarkState,freq[benchmarkState]))
                state += 1  # move to the next target point
                # if the path is finished, set the home position as the next goal point
                if state == len(pointsX):
                    state = 0
                # if the benchmark is finished, sdo not display the next point
                if benchmarkState < len(freq):
                    print('    >>> Step to point {} <<<'.format(state))

            # apply magnetic field
            t = time.time() - startTime # elapsed time (sec)
            theta = 2 * pi * freq[benchmarkState] * t
            fieldX = magnitude * cos(theta) * cosd(angle+60)
            fieldY = magnitude * cos(theta) * sind(angle+60)
            fieldZ = magnitude * sin(theta)
            self.field.setX(fieldX)
            self.field.setY(fieldY)
            self.field.setZ(fieldZ)
            if self.stopped or benchmarkState == len(freq):
                return

    def examplePiecewiseFunction(self):
        """
        This function shows an example of a piecewise function.
        It first convert time into normalizedTime (range [0,1)).
        Values are selected based on *normT*.
        This makes it easier to change frequency without modifying the shape of the funciton.
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
