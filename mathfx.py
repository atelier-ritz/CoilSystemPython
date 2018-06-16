from math import pi, sin, cos, radians, sqrt
def cosd(val):
    return cos(radians(val))

def sind(val):
    return sin(radians(val))

def oscBetween(currentTime,oscShape,frequency,bound1,bound2,phaseOffset=0):
    """
          /\    /\    /\     < ‾ ‾ ‾ upperbound
         /  \  /  \  /  \
        /    \/    \/    \   < _ _ _ lowerbound

    This is a function that returns a value that oscillates periodically between a lower and an upper bound.
    It always returns "lowerBound" when currentTime = 0
    @param currentTime: elapsed time (s), the x-axis variable of the periodical function
    @param oscShape: defines the waveform of the oscillation
    @param phaseOffset: defines the offset of the phase (range: 0 to 1)
        0 or 1: no phase offset
        0.5: half period delay
        0.25: quarter period delay
    @return: the value of the periodical function
    """
    if frequency == 0 or bound1 == bound2:
        return 0
    if bound1 > bound2:
        lowerBound, upperBound = bound2, bound1
    else:
        lowerBound, upperBound = bound1, bound2
    time = currentTime + 1/frequency*phaseOffset
    if oscShape == 'sin':
        return 0.5 * (lowerBound+upperBound) + (upperBound-lowerBound)*0.5 * sin(2*pi*frequency*(time-0.25/frequency))
    elif oscShape == 'saw':
        return lowerBound + time*frequency*(upperBound-lowerBound) % (upperBound-lowerBound)
    elif oscShape == 'square':
        return lowerBound if int(frequency * 2 * time) % 2 == 0 else upperBound
    elif oscShape == 'triangle':
        return lowerBound + abs((lowerBound-upperBound) + (time+0.5/frequency)*frequency*2*(upperBound-lowerBound) % (2*(upperBound-lowerBound)))
    else:
        return 0

def normalizeTime(currentTime,frequency):
    '''
    This function converts the x-axis variable (time) of a periodic function to the normalized time, range: 0 - 1
    '''
    if frequency == 0: return 0
    else:
        period = 1/frequency
        return currentTime % period / period

def perpendicularFootToLine(x,y,x1,y1,x2,y2):
    """
    A line *l* is defined by P1(x1,y1) and P2(x2,y2). (Ax + By + C = 0)
    A point *P* is defined by (x,y).
    This function returns the perpendicular foot of the point *P* to the line *l*.
    """
    A = y2 - y1
    B = x1 - x2
    C = y1 * (x2 - x1) - x1 * (y2 - y1)
    footX = (B**2*x - A*B*y - A*C) / (A**2 + B**2)
    footY = (A**2*y - A*B*x - B*C) / (A**2 + B**2)
    return footX, footY

def distanceBetweenPoints(x1,y1,x2,y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

def normalizeAngle(radians):
    """
    Normalize angles to (-pi,pi]
    """
    angle = radians % (2*pi) # [0,2*pi)
    if angle > pi: angle = angle - 2*pi
    return angle
