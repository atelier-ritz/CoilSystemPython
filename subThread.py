import time
from math import pi, sin, cos
from PyQt5.QtCore import pyqtSignal, QMutexLocker, QMutex, QThread


class SubThread(QThread):
    statusSignal = pyqtSignal(str)

    def __init__(self,field,vision,parent=None,):
        super(SubThread, self).__init__(parent)
        self.stopped = False
        self.mutex = QMutex()
        self.field = field
        self.vision = vision

        self.freq = 0

    def setup(self):
        self.stopped = False

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stopped = True

    def run(self):
        # self.taskTest()
        self.taskSinFieldXY()
        self.stop()
        self.finished.emit()

    #====================================
    # Task Example
    # print elapsed time every 2 seconds and emit a signal to GUI
    #====================================
    def taskTest(self):
        counter = 1
        while True:
            time.sleep(1)
            counter += 1
            if counter % 2 == 0:
                sendStr = 'Time elapsed: {}s'.format(counter)
                self.statusSignal.emit(sendStr)
            if self.stopped:
                return
    #====================================
    # Task Example 2
    # Apply a rotational magnetic field in X-Y plane
    #====================================
    def setFreq(self,Hz):
        self.freq = Hz

    def taskSinFieldXY(self):
        startTime = time.time()
        while True:
            t = time.time() - startTime # elapsed time (sec)
            theta = 2 * pi * self.freq * t
            fieldX = 2 * cos(theta)
            fieldY = 2 * sin(theta)
            self.field.setX(fieldX)
            self.field.setY(fieldY)
            if self.stopped:
                return
