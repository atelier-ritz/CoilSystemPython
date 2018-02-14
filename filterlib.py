import cv2

#========================================
# Usage: grey()
#========================================
def grey(inputImage,args=''):
    return cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)

#========================================
# threshold(lowerBound,higherBound)
# Input must be a greyscale image
#========================================
def threshold(inputImage,args):
    arg = args.split(',')
    ret, _ = cv2.threshold(inputImage,int(arg[0]),int(arg[1]),cv2.THRESH_BINARY)
    return ret

#========================================
# canny(minVal,maxVal)
# Input must be a greyscale image
#========================================
def canny(inputImage,args):
    arg = args.split(',')
    return cv2.Canny(inputImage,int(arg[0]),int(arg[1]))
