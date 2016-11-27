import cv2
import os
import random
import numpy as np

#print "working directory: "
#print os.getcwd()


def convex_area_diff (contour):

    xks = [point[0][0] for point in contour]
    yks = [point[0][1] for point in contour]

    rectangle_area = (max(xks) - min(xks)) * (max(yks) - min(yks))
    area = cv2.contourArea(contour)

    return float((rectangle_area - area))/rectangle_area


def ratio(contour):
    """  """
    xks = [point[0][0] for point in contour]
    yks = [point[0][1] for point in contour]

    diff_x = max(xks) - min(xks)
    diff_y = max(yks) - min(yks)

    if diff_y == 0:
        return float('inf')
    else:
        return float(diff_x) / float(diff_y)


def is_not_too_small(contour):
    xks = [point[0][0] for point in contour]
    yks = [point[0][1] for point in contour]

    diff_x = max(xks) - min(xks)
    diff_y = max(yks) - min(yks)

    return diff_x > 40 and diff_y > 20



######################
expected_ratio = 520.0 / 114.0


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
        srcImage = cv2.imread( filePath, 0 )
        colorImage = cv2.imread( filePath, cv2.cv.CV_LOAD_IMAGE_COLOR )
        threshholding = cv2.adaptiveThreshold( srcImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2 )
        
        #cv2.imshow( "src", srcImage )
        #cv2.imshow( "copy", colorImage )
        
        contours, hierarchy = cv2.findContours( threshholding, cv2.cv.CV_RETR_LIST , cv2.cv.CV_CHAIN_APPROX_NONE )

        # The license plate:
        #     must be at least a rectangle
        #     should have width to height ratio as defined in the traffic law
        #     should be at least 30x15px
        filtered_contours = [contour for contour in contours
                             if len(contour) >= 4 and
                             abs(ratio(contour) - expected_ratio) < 1 and
                             is_not_too_small(contour)]

        # It's a good idea to simplify the contours to their convex hulls.
        simplified_contours = [cv2.convexHull(contour) for contour in filtered_contours]

        if not len(simplified_contours) == 0:
            # For now, we select "the most rectangular" contour.
            # There should be a threshold to find more license plates.
            selected_contours = [sorted(simplified_contours, key=convex_area_diff)[0]]

            for contour in simplified_contours:
                print(convex_area_diff(contour))

            for idx in range( 0, len( selected_contours ) ):
                R = random.randint( 0, 255 )
                G = random.randint( 0, 255 )
                B = random.randint( 0, 255 )

                cv2.drawContours( colorImage, selected_contours, idx, ( R, G, B ), cv2.cv.CV_FILLED )

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
