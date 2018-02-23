import cv2
import numpy as np

#=============================================================================================
# Call this function if selected algorithm is not defined
#=============================================================================================
def algorithmNotDefined(imageFiltered,imageOriginal,*args):
    print('Algorithm name not defined in objectDetection.py')
    return imageOriginal

#====================================================
# Use binary image as input in this algorithm
# Detect the biggest contour (except the edge of the screen)
#====================================================
def algorithmA(imageFiltered,imageOriginal,agent):
    nOfSamples = 2
    im2, contours, hierarchy = cv2.findContours(imageFiltered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:nOfSamples]
    if len(cnts) > 1:
        targetCnt = cnts[1] # cnt[0] is the edge of the screen
        rect = cv2.minAreaRect(targetCnt)
        box = np.int0(cv2.boxPoints(rect)) # vertices of the bounding rect
        center = np.int0(np.sum(box, axis=0)/4) # [centerX, centerY] dataType: int
        agent.set(center[0],center[1]) # update the position of the agnet
        imageOriginal = cv2.drawContours(imageOriginal,[box],0,(0,255,0), 3) # draw boundingRect on the original image
    return imageOriginal

class Agent():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.orientation = 0

    def set(self,x,y,orientation = 0):
        self.x = x
        self.y = y
        self.orientation = orientation
