# Used for drawing plots on the frames for general purposes
# but not related to object detection

import cv2

#=============================================================================================
# Call this function if selected drawingName is not defined
#=============================================================================================
def drawingNotDefined(img,args):
    print('Drawing not defined in drawing.py')
    return img

#=============================================================================================
# Pass a list as args
#=============================================================================================
def circle(img,args):
    x, y, r = args
    cv2.circle(img, (x,y), r, (0,0,255), 2)
    return img

def arrow(img,args):
    x1,y1,x2,y2 = args
    cv2.arrowedLine(img, (x1,y1), (x2,y2), (0,255,0), 1)
    return img

def line(img,args):
    x1,y1,x2,y2 = args
    cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 2)
    return img

def pathUT(img,args):
    pathID, offsetX, offsetY, scale, _ = args
    if pathID == 0:
        points = [(10,10),(10,400),(150,400),(150,10)]
        points = [(int(point[0]+offsetX),int(point[1]+offsetY)) for point in points]
        for i in range(len(points)-1):
            cv2.line(img, points[i], points[i+1], (255,0,0), 2)
    elif pathID == 1:
        points = [(180,10),(250,10),(250,400),(250,10),(320,10)]
        points = [(int(point[0]+offsetX),int(point[1]+offsetY)) for point in points]
        for i in range(len(points)-1):
            cv2.line(img, points[i], points[i+1], (255,0,0), 2)
    return img

def closedPath(img,args):
    pointsX = args[0] # [x1,x2,....]
    pointsY = args[1] # [y1,y2,....]
    for i in range(len(pointsX)-1):
        cv2.line(img, (pointsX[i],pointsY[i]), (pointsX[i+1],pointsY[i+1]), (0,255,0), 2)
    return img
