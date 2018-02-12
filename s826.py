from ctypes import cdll
s826dll = cdll.LoadLibrary("./lib826_64.so")

class S826(object):
    def __init__(self):
        self._flag = 0
        errcode = self.s826_init()
        if errcode != 1:
            print('Cannot detect s826 board. Error code: {}'.format(errcode))
            self.s826_close()

    def s826_init(self):
        errCode = s826dll.S826_SystemOpen()
        return errCode

    def s826_close(self):
        s826dll.S826_SystemClose()

    # ======================================================================
    # Set 1 AO channel.
    # Input: board: board identifier.
    # chan : DAC channel # in the range 0 to 7.
    # rangeCode: 0: 0 +5V; 1: 0 +10V; 2: -5 +5V; 3:-10 +10V.
    # outputV: Desired analog output voltage (can be positive and negative).
    # ======================================================================
    def s826_aoPin(self,chan,rangeCode,outputV):
        lowerV = -5
        rangeV = 10
        BOARD = 0
        setpoint = int((outputV-lowerV)/rangeV*0xffff)
        s826dll.S826_DacRangeWrite(BOARD,chan,rangeCode,0)
        s826dll.S826_DacDataWrite(BOARD,chan,setpoint,0)
