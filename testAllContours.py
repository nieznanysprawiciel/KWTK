import cv2
import os
import random
import numpy as np
import processing

#print "working directory: "
#print os.getcwd()


def convex_area_diff (contour):

    xks = [point[0][0] for point in contour]
    yks = [point[0][1] for point in contour]

    rectangle_area = (max(xks) - min(xks)) * (max(yks) - min(yks))
    area = cv2.contourArea(contour)

    return float((rectangle_area - area))/rectangle_area


######################



imagesDir = "images/"
thresholdDir = "thresh/"
contoursDir = "contours/"

writeExtension = ".jpg"        # for unknown reasons sometimes python can't write image with jpg or png extension :(

imageName = "auto000.jpg"
filePath = imagesDir + imageName

if not os.path.exists( contoursDir ):
    os.makedirs( contoursDir )
    print "Created directory: " + contoursDir

# initialize of random numbers
random.seed()

imageFiles = os.listdir( imagesDir )

for image in imageFiles:

    filePath = imagesDir + image

    if os.path.isfile( filePath ):   
        colorImage = cv2.imread( filePath, cv2.cv.CV_LOAD_IMAGE_COLOR )

        #if processing.process( colorImage ):
        if processing.process_area_only( colorImage ):
            #cv2.imshow( filePath, colorImage )

            pre, ext = os.path.splitext( image )
            image = pre + writeExtension
            resultFile = contoursDir + image

            cv2.imwrite( resultFile, colorImage )
            print "Segmented image result in: " + resultFile
        #else:
            #raise Exception("No license plate found!")
            
    else:
        print "Image doesn't exist: " + filePath

cv2.waitKey(0)
cv2.destroyAllWindows()
        
#
