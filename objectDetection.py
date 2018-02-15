import cv2

#====================================================
# ALWAYS use binary image as input in this algorithm
#====================================================
def algorithmA(self,imageFiltered,imageOriginal,agent):
    im2, contours, hierarchy = cv2.findContours(imageFiltered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[4]
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(imageOriginal,(x,y),(x+w,y+h),(0,255,0),2)
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
