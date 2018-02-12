import os, sys, time
from PyQt5.QtCore import pyqtSignal, QMutexLocker, QMutex, QThread


class SubThread(QThread):
    statusSignal = pyqtSignal(str)
    def __init__(self,field,vision,parent=None,):
        super(SubThread, self).__init__(parent)
        self.stopped = False
        self.mutex = QMutex()
        self.field = field
        self.vision = vision

    def setup(self):
        self.stopped = False

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stopped = True

    def run(self):
        counter = 1
        while True:
            time.sleep(1)
            counter += 1
            if counter % 2 == 0:
                sendStr = 'Time elapsed: {}s'.format(counter)
                self.statusSignal.emit(sendStr)
            if self.stopped:
                return
        self.stop()
        self.finished.emit()
