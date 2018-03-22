from math import pi, sin, cos, radians
def cosd(a):
    return cos(radians(a))

def sind(a):
    return sin(radians(a))

def oscBetween(currentTime,oscShape,frequency,lowerBound,upperBound):
    ''' allows oscillation between lowerBound and upperBound '''
    if oscShape == 'sin':
        return 0.5 * (lowerBound+upperBound) + (upperBound-lowerBound)*0.5 * sin(2*pi*frequency*currentTime)
    elif oscShape == 'saw':
        return lowerBound + currentTime*frequency*(upperBound-lowerBound) % (upperBound-lowerBound)
    elif oscShape == 'square':
        return upperBound if int(frequency * 2 * t) % 2 == 0 else lowerBound
    elif oscShape == 'triangle':
        return lowerBound + abs((lowerBound-upperBound) + currentTime*frequency*2*(upperBound-lowerBound) % (2*(upperBound-lowerBound)))
    else:
        return 0
