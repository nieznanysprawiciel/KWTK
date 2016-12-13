import cv2
import random
import numpy as np
import filters


def top_left_compare ( point ):
    return point[ 0 ][ 0 ] + point[ 0 ][ 1 ]

def top_right_compare( point ):
    return point[ 0 ][ 0 ] - point[ 0 ][ 1 ]


def find_corners ( contour ):
    """
    Compute dot product between edge vectors and each contour point
    """

    top_left = min( contour, key = top_left_compare )
    top_right = max( contour, key = top_right_compare )
    bottom_right = max( contour, key = top_left_compare )
    bottom_left = min( contour, key = top_right_compare )


    return top_left, top_right, bottom_right, bottom_left


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
        
        
def compute_contour_weight( index, hierarchy ):
    num_letters = 7
    
    num_sub_objects = filters.count_sub_object( index, hierarchy )
    print num_sub_objects
    
    difference = float( num_sub_objects - num_letters )
    difference = min( abs( difference ), num_letters )
    weight = 1 - difference / num_letters
    
    return weight
    
    
def get_children( index, hierarchy, contours ):
    first_child_idx = hierarchy[ index ][ 2 ]    # Check openCV docs
    
    child_list = []
    
    if first_child_idx < 0:
        return child_list
    
    while hierarchy[ first_child_idx ][ 0 ] >= 0:
        first_child_idx = hierarchy[ first_child_idx ][ 0 ]
        child_list.append( contours[ first_child_idx ] )
    
    return child_list
    
    

### main function in this file
def process( colorImage ):

    srcImage = cv2.cvtColor( colorImage, cv2.COLOR_BGR2GRAY )
    threshholding = cv2.adaptiveThreshold( srcImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 5 )
    
    contours, hierarchy = cv2.findContours( threshholding, cv2.cv.CV_RETR_TREE , cv2.cv.CV_CHAIN_APPROX_NONE )
    filtered_contours, contoursIndiecies = filters.filter_contours( contours, hierarchy )
                         

    # It's a good idea to simplify the contours to their convex hulls.
    simplified_contours = [cv2.convexHull(contour) for contour in filtered_contours]

    if not len( simplified_contours ) == 0:
        # For now, we select "the most rectangular" contour.
        # There should be a threshold to find more license plates.
        #selected_contours = [sorted(simplified_contours, key=convex_area_diff)[0]]
        
        area_weights = [ convex_area_diff( contour ) for contour in simplified_contours ]
        hierarchy_weights = [ compute_contour_weight( idx, hierarchy[ 0 ] ) for idx in contoursIndiecies ]
        weights_sum = [sum(x) for x in zip(area_weights, hierarchy_weights)]
        
        best = max( weights_sum )
        best_idx = weights_sum.index( best )

        for weight in weights_sum:
            print(weight)        
        
        for contour in simplified_contours:
            print(convex_area_diff(contour))

        result = [ simplified_contours[ best_idx ] ]
        draw_contours( result, colorImage )
        
        result_children = get_children( contoursIndiecies[ best_idx ], hierarchy[ 0 ], contours )
        draw_contours( result_children, colorImage )
        
        return True
    else:
        return False
        
		
def process_area_only( colorImage ):

    srcImage = cv2.cvtColor( colorImage, cv2.COLOR_BGR2GRAY )
    threshholding = cv2.adaptiveThreshold( srcImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 5 )
    
    contours, hierarchy = cv2.findContours( threshholding, cv2.cv.CV_RETR_TREE , cv2.cv.CV_CHAIN_APPROX_NONE )
    filtered_contours, contoursIndiecies = filters.filter_contours( contours, hierarchy )
                         

    # It's a good idea to simplify the contours to their convex hulls.
    simplified_contours = [cv2.convexHull(contour) for contour in filtered_contours]

    if not len( simplified_contours ) == 0:
        # For now, we select "the most rectangular" contour.
        # There should be a threshold to find more license plates.
        selected_contours = [sorted(simplified_contours, key=convex_area_diff)[0]]

        draw_contours( selected_contours, colorImage )
        
        return True
    else:
        return False