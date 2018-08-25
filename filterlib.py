import cv2

#=============================================================================================
# Call this function if selected filterName is not defined
#=============================================================================================
def filterNotDefined(inputImage,args=None):
    print('Filter name not defined in filterlib.py')
    return inputImage

#========================================
# Usage: grey()
# convert to grey image
#========================================
def grey(inputImage,args=None):
    if len(inputImage.shape) == 3:
        return cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
    else:
        return inputImage

#========================================
# Usage: color()
# convert to color image
#========================================
def color(inputImage,args=None):
    if len(inputImage.shape) == 2:
        return cv2.cvtColor(inputImage, cv2.COLOR_GRAY2BGR)
    else:
        return inputImage

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

#========================================
# erode(img, kernel, iterations=1)
# Input must be a binary image
#========================================
def erode(inputImage,args):
    arg = args.split(',')
    kernel = np.ones((int(arg[0]),int(arg[0])), np.uint8)
    return cv2.erode(inputImage, kernel, iterations=1)

#========================================
# dilate(img, kernel, iterations=1)
# Input must be a binary image
#========================================
def dilate(inputImage,args):
    arg = args.split(',')
    kernel = np.ones((int(arg[0]),int(arg[0])), np.uint8)
    return cv2.dilate(inputImage, kernel, iterations=1)
