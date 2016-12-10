import cv2
import random
import numpy as np
import filters

def convex_area_diff (contour):

    xks = [point[0][0] for point in contour]
    yks = [point[0][1] for point in contour]

    rectangle_area = (max(xks) - min(xks)) * (max(yks) - min(yks))
    area = cv2.contourArea(contour)

    return float((rectangle_area - area))/rectangle_area


def draw_contours( contours, colorImage ):
    
    for idx in range( len( contours ) ):
        R = random.randint( 0, 255 )
        G = random.randint( 0, 255 )
        B = random.randint( 0, 255 )

        cv2.drawContours( colorImage, contours, idx, ( R, G, B ), cv2.cv.CV_FILLED )
        
        

### main function in this file
def process( colorImage ):

    srcImage = cv2.cvtColor( colorImage, cv2.COLOR_BGR2GRAY )
    threshholding = cv2.adaptiveThreshold( srcImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2 )
    
    contours, hierarchy = cv2.findContours( threshholding, cv2.cv.CV_RETR_TREE , cv2.cv.CV_CHAIN_APPROX_NONE )
    filtered_contours, filtered_hierarchy = filters.filter_contours( contours, hierarchy )
                         

    # It's a good idea to simplify the contours to their convex hulls.
    simplified_contours = [cv2.convexHull(contour) for contour in filtered_contours]

    if not len( simplified_contours ) == 0:
        # For now, we select "the most rectangular" contour.
        # There should be a threshold to find more license plates.
        selected_contours = [sorted(simplified_contours, key=convex_area_diff)[0]]

        for contour in simplified_contours:
            print(convex_area_diff(contour))

        draw_contours( selected_contours, colorImage )
        return True
    else:
        return False
        
    