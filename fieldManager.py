from ctypes import cdll
s826dll = cdll.LoadLibrary("./lib826_64.so")

# assign pin # to the coil
PIN_X1 = 0
PIN_X2 = 3
PIN_Y1 = 1
PIN_Y2 = 4
PIN_Z1 = 2
PIN_Z2 = 5

class FieldManager(object):
    def __init__(self,dac):
        self.x = 0
        self.y = 0
        self.z = 0
        self.dac = dac

    def setX(self,mT):
        self.dac.s826_aoPin(PIN_X1,2,mT/5.003)
        self.dac.s826_aoPin(PIN_X2,2,mT/4.879)
        self.x = mT

    def setY(self,mT):
        self.dac.s826_aoPin(PIN_Y1,2,mT/5.024)
        self.dac.s826_aoPin(PIN_Y2,2,mT/5.143)
        self.y = mT

    def setZ(self,mT):
        self.dac.s826_aoPin(PIN_Z1,2,mT/5.024)
        self.dac.s826_aoPin(PIN_Z2,2,mT/4.433)
        self.z = mT

    def setXYZ(self,x_mT,y_mT,z_mT):
        self.setX(x_mT)
        self.setY(y_mT)
        self.setZ(z_mT)
