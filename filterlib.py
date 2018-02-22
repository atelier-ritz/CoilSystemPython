import cv2

#========================================
# Usage: grey()
#========================================
def grey(inputImage,args=''):
    return cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)

#========================================
# Usage: blur(radius)
# Since only odd number is allowed in Gaussian blur,
# we use 2*n+1 as the radius
#========================================
def blur(inputImage,args):
    arg = args.split(',')
    return cv2.GaussianBlur(inputImage,(int(arg[0])*2+1,int(arg[0])*2+1),0)

#========================================
# threshold(lowerBound,higherBound)
# Input must be a greyscale image
#========================================
def threshold(inputImage,args):
    arg = args.split(',')
    _, ret = cv2.threshold(inputImage,int(arg[0]),int(arg[1]),cv2.THRESH_BINARY)
    return ret

#========================================
# canny(minVal,maxVal)
# Input must be a greyscale image
#========================================
def canny(inputImage,args):
    arg = args.split(',')
    return cv2.Canny(inputImage,int(arg[0]),int(arg[1]))
