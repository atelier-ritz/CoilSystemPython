import cv2, math
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
def detectBiggestContour(imageFiltered,imageOriginal,agent):
    nOfSamples = 2
    im2, contours, hierarchy = cv2.findContours(imageFiltered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:nOfSamples]
    if len(cnts) > 1:
        targetCnt = cnts[1] # cnt[0] is the edge of the screen
        rect = cv2.minAreaRect(targetCnt) # (x,y)(w,h)theta
        box = np.int0(cv2.boxPoints(rect)) # vertices of the bounding rect
        center = np.int0(np.sum(box, axis=0)/4) # [centerX, centerY] dataType: int
        agent.set(center[0],center[1],rect[2]) # update the position of the agnet
        cv2.drawContours(imageOriginal,[box],0,(0,255,0), 3) # draw boundingRect on the original image
        print(rect[2])
    return imageOriginal

#====================================================
# Use binary image as input in this algorithm
# Detect all contours and use PCA to find the orientation
#====================================================
def drawAxis(img, start_pt, vec, colour, length):
    CV_AA = 16 # antialias
    end_pt = (int(start_pt[0] + length * vec[0]), int(start_pt[1] + length * vec[1]))
    cv2.circle(img, (int(start_pt[0]), int(start_pt[1])), 5, colour, 2)
    cv2.line(img, (int(start_pt[0]), int(start_pt[1])), end_pt, colour, 2, CV_AA);
    angle = math.atan2(vec[1], vec[0])

    qx0 = int(end_pt[0] - 9 * math.cos(angle + math.pi / 4));
    qy0 = int(end_pt[1] - 9 * math.sin(angle + math.pi / 4));
    cv2.line(img, end_pt, (qx0, qy0), colour, 1, CV_AA);

    qx1 = int(end_pt[0] - 9 * math.cos(angle - math.pi / 4));
    qy1 = int(end_pt[1] - 9 * math.sin(angle - math.pi / 4));
    cv2.line(img, end_pt, (qx1, qy1), colour, 1, CV_AA);


def primaryComponentAnalysis(imageFiltered,imageOriginal,agent):
    #   cv2.CHAIN_APPROX_NONE       save all points
    #   cv2.CHAIN_APPROX_SIMPLE     only save key points
    img, contours, hierarchy = cv2.findContours(imageFiltered, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for i in range(0, len(contours)):
        area = cv2.contourArea(contours[i])# calculate contour area
        if area < 1e2 or 1e5 < area:    # get rid of small areas (noise) and big areas (the edges of the screen)
            continue
        cv2.drawContours(imageOriginal, contours, i, (0, 255, 0), 2, 8, hierarchy, 0)
        X = np.array(contours[i], dtype=np.float).reshape((contours[i].shape[0], contours[i].shape[2])) # save contour as float array
        mean, eigenvectors = cv2.PCACompute(X, mean=np.array([], dtype=np.float), maxComponents=1) # one-dimensioanl Primary Component Analysis
        pt = (mean[0][0], mean[0][1])
        vec = (eigenvectors[0][0], eigenvectors[0][1]) # eigen vectors
        drawAxis(imageOriginal, pt, vec, (0, 0, 255), 150)
        angle = math.atan2(-vec[1], vec[0])
    return imageOriginal

#====================================================
# Etc..
#====================================================



class Agent():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.orientation = 0

    def set(self,x,y,orientation = 0):
        self.x = x
        self.y = y
        self.orientation = orientation
