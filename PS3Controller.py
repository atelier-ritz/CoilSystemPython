import pygame, time, math
from mathfx import sind, cosd

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

'''
PS3 Controllers can be turned on by presing PS button.
If you see one solid indicator light, it is on.
If you see four lights blinking it is off.
'''

class DualShock(object):
    KEY = {
        'CROSS': 0,
        'CIRCLE': 1,
        'TRIANGLE': 2,
        'SQUARE': 3,
        'L1': 4,
        'R1': 5,
        'L2': 6,
        'R2': 7,
        'SELE': 8,
        'START': 9,
        'PS': 10,
        'L3': 11,
        'R3': 12
    }
    AXIS = {
        'L_X': 0,
        'L_Y': 1,
        'L2': 2,
        'R_X': 3,
        'R_Y': 4,
        'R2': 5
    }

    def __init__(self):
        self._name = joystick.get_name()
        self._numAxes = joystick.get_numaxes()
        self._numButtons = joystick.get_numbuttons()
        self.axis_data = {}
        self.button_data = {}
        for i in range(self._numAxes): self.axis_data[i] = 0.0
        self.axis_data[2] = -1.0
        self.axis_data[5] = -1.0
        for i in range(self._numButtons): self.button_data[i] = False
        self.showInfo()

    def quit(self):
        pygame.joystick.quit()
        pygame.quit()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self.axis_data[event.axis] = round(event.value,2)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.button_data[event.button] = True
            elif event.type == pygame.JOYBUTTONUP:
                self.button_data[event.button] = False

    def isPressed(self,keycode):
        return self.button_data[self.KEY[keycode]]

    def getAngleLeft(self):
        rad = math.atan2(-self.axis_data[1],self.axis_data[0])
        return math.degrees(rad)

    def getTiltLeft(self):
        azimuth = abs(self.getAngleLeft())
        magnitude = self.getMagniudeLeft()
        if magnitude == 0:
            return 90
        if azimuth < 45:
            magnitudeMax = 1 / cosd(azimuth)
        elif azimuth < 90:
            magnitudeMax = 1 / cosd(90-azimuth)
        elif azimuth < 135:
            magnitudeMax = 1 / cosd(azimuth-90)
        elif azimuth <= 180:
            magnitudeMax = 1 / cosd(180-azimuth)
        ratio = self.getMagniudeLeft() / magnitudeMax
        if ratio > 1: ratio = 1
        return math.degrees(math.acos(ratio))

    def getMagniudeLeft(self):
        return math.sqrt(self.axis_data[0]**2 + self.axis_data[1]**2)

    def getAngleRight(self):
        rad = math.atan2(-self.axis_data[4],self.axis_data[3])
        return math.degrees(rad)

    def getMagniudeRight(self):
        return math.sqrt(self.axis_data[3]**2 + self.axis_data[4]**2)

    def getStick(self,index):
        raw = self.axis_data[index]
        if index == 1 or index == 4: # leftY or rightY
            return -raw
        elif index == 0 or index == 3: # leftX or rightX
            return raw
        elif index == 2 or index == 5: # L2 or R2
            return raw
        else:
            return raw * 0.5 + 0.5 # map the value to 0(released)-1(pressed)

    def showInfo(self):
        print("===========================================")
        print('Name: {}'.format(self._name))
        print('Axes: {}'.format(self._numAxes))
        print('Buttons: {}'.format(self._numButtons))
        print("===========================================")

if __name__ == "__main__":
    ''' Run this script directly for testing '''
    import time
    j = DualShock()
    while True:
        j.update()
        print(j.axis_data)
        print(j.button_data)
        time.sleep(0.1)
