from ctypes import cdll
s826dll = cdll.LoadLibrary("./lib826_64.so")
BOARD = 0
RANGE_PARAM = [[0,5],[0,10],[-5,10],[-10,20]] # rangeCode = 0, 1, 2, 3     [lowerV,rangeV]



class S826(object):
    def __init__(self):
        self.lowerV = [-5,-5,-5,-5,-5,-5,-5,-5]  # default range selection = 2
        self.rangeV = [10,10,10,10,10,10,10,10]  # default range selection = 2
        errcode = self.s826_init()
        if errcode != 1:
            print('Cannot detect s826 board. Error code: {}'.format(errcode))
            self.s826_close()
            return
        self.s826_initRange()

    def s826_init(self):
        errCode = s826dll.S826_SystemOpen()
        return errCode

    def s826_close(self):
        s826dll.S826_SystemClose()

    def s826_initRange(self):
        for i in range(8):
            self.s826_setRange(i,2)

    # ======================================================================
    # rangeCode: 0: 0 +5V; 1: 0 +10V; 2: -5 +5V; 3:-10 +10V.
    # ======================================================================
    def s826_setRange(self,chan,rangeCode):
        self.lowerV[chan] = RANGE_PARAM[rangeCode][0]
        self.rangeV[chan] = RANGE_PARAM[rangeCode][1]
        s826dll.S826_DacRangeWrite(BOARD,chan,rangeCode,0) # BOARD, chan, rangeCode, output V

    # ======================================================================
    # Set 1 AO channel.
    # chan : DAC channel # in the range 0 to 7.
    # outputV: Desired analog output voltage (can be positive and negative).
    # ======================================================================
    def s826_aoPin(self,chan,outputV):
        lowerV = self.lowerV[chan]
        rangeV = self.rangeV[chan]
        setpoint = int((outputV-lowerV)/rangeV*0xffff)
        s826dll.S826_DacDataWrite(BOARD,chan,setpoint,0)
