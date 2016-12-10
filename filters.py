import cv2
import numpy as np
import random

#### global
expected_ratio = 520.0 / 114.0


### functions

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

    
def count_sub_object( index, hierarchy ):
    num_sub_objects = 0
    first_child_idx = hierarchy[ index ][ 2 ]    # Check openCV docs
    
    if first_child_idx < 0:
        return 0
    
    while hierarchy[ first_child_idx ][ 0 ] >= 0:
        first_child_idx = hierarchy[ first_child_idx ][ 0 ]
        num_sub_objects = num_sub_objects + 1
        
    return num_sub_objects
    
def has_letters_inside( index, hierarchy, min, max ):
    min_letters = min
    max_letters = max

    num_sub_objects = count_sub_object( index, hierarchy )
    
    return num_sub_objects >= min_letters or num_sub_objects <= max_letters
    
    
### main function
    
def filter_contours( contours, hierarchy ):
        hierarchy = hierarchy[ 0 ]

        # The license plate:
        #     must be at least a rectangle
        #     should have width to height ratio as defined in the traffic law
        #     should be at least 30x15px
        #     should contain letters
        contoursIndiecies = [ idx for idx in range( len( contours ) )
                             if len(contours[ idx ]) >= 4 and
                             abs(ratio(contours[ idx ]) - expected_ratio) < 1 and
                             is_not_too_small(contours[ idx ]) ]#and
                             #has_letters_inside( idx, hierarchy, 5, 9 ) ]
        
        #print contoursIndiecies
        
        #if len( contoursIndiecies ) > 0:
        newContours = [ contours[ contoursIndiecies[ idx ] ] for idx in range( len( contoursIndiecies ) ) ]
        #newHierarchy = [ hierarchy[ contoursIndiecies[ idx ] ] for idx in range( len( contoursIndiecies ) ) ]
        
        return newContours, contoursIndiecies
        
        