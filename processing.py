import cv2
import logging
import random
import numpy as np
import filters
import matplotlib.pyplot as plt


logger = logging.getLogger(__name__)


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


    return np.array([top_left, top_right, bottom_right, bottom_left])
######

def perspective_warping ( rect, orig):

    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))


    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))


    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))

    # construct our destination points which will be used to
    # map the screen to a top-down, "birds eye" view
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]],
        dtype="float32")

    # calculate the perspective transform matrix and warp
    # the perspective to grab the screen
    M = cv2.getPerspectiveTransform(rect, dst)
    warp = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))

    return warp


######

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
    logger.info("Number of subobjects: " + str(num_sub_objects))
    
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
    
    contours, hierarchy = cv2.findContours( threshholding, cv2.cv.CV_RETR_TREE , cv2.cv.CV_CHAIN_APPROX_SIMPLE )
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
            logger.info("Weight: " + str(weight))
        
        for contour in simplified_contours:
            logger.info("Convex area diff: " + str(convex_area_diff(contour)))

        result = [ simplified_contours[ best_idx ] ]
        draw_contours( result, colorImage )
        
        result_children = get_children( contoursIndiecies[ best_idx ], hierarchy[ 0 ], contours )
        draw_contours( result_children, colorImage )
        
        return True
    else:
        return False
        
        
def process_area_only2(colorImage, adaptive_thresholding_block_size, adaptive_thresholding_constant):

    srcImage = cv2.cvtColor( colorImage, cv2.COLOR_BGR2GRAY )
    threshholding = cv2.adaptiveThreshold(
        srcImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
        adaptive_thresholding_block_size, adaptive_thresholding_constant)
    
    contours, hierarchy = cv2.findContours( threshholding, cv2.cv.CV_RETR_TREE , cv2.cv.CV_CHAIN_APPROX_NONE )
    filtered_contours, contoursIndiecies = filters.filter_contours( contours, hierarchy )
                         

    # It's a good idea to simplify the contours to their convex hulls.
    simplified_contours = [cv2.convexHull(contour) for contour in filtered_contours]

    if not len( simplified_contours ) == 0:
        # For now, we select "the most rectangular" contour.
        # There should be a threshold to find more license plates.
        selected_contours = [sorted(simplified_contours, key=convex_area_diff)[0]]

        corners = [find_corners(contour) for contour in selected_contours]

        #print corners
        #draw_contours( selected_contours, colorImage )
        #draw_contours(corners, colorImage)

        rect = np.array([point[0] for point in corners[0]], dtype="float32")
        print rect
        warped = perspective_warping(rect, colorImage)

        # sheared_plate = perspective_warping(corners, threshholding)
        # cv2.imshow(sheared_plate)

        return warped
    else:
        logger.info( "All contours filtered out" )
        return None

        
def process_chosen_contour(colorImage, corners, adaptive_thresholding_block_size, adaptive_thresholding_constant):
              
    rect = np.array([point[0] for point in corners[0]], dtype="float32")
    print rect
    warped = perspective_warping(rect, colorImage)

    return warped


def drawing_segments_histograms(horizontal_crop, vertical_crop, saveFileHorizontal, saveFileVertical):

    fig = plt.figure()
    plt.plot(horizontal_crop)
    plt.xlabel('Piksele')
    plt.ylabel('Intensywnosc')
    plt.title('Horizontal histogram ')
    plt.axis()
    plt.grid(True)
    fig.savefig(saveFileHorizontal, format='jpg', dpi=60)

    fig = plt.figure()
    plt.plot(vertical_crop)
    plt.xlabel('Piksele')
    plt.ylabel('Intensywnosc')
    plt.title('Vertical histogram ')
    plt.axis()
    plt.grid(True)
    fig.savefig(saveFileVertical, format='jpg', dpi=60)


def process_area_only(colorImage):

    srcImage = cv2.cvtColor(colorImage, cv2.COLOR_BGR2GRAY)
    threshholding = cv2.adaptiveThreshold(srcImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 5)

    contours, hierarchy = cv2.findContours(threshholding, cv2.cv.CV_RETR_TREE, cv2.cv.CV_CHAIN_APPROX_NONE)
    filtered_contours, contoursIndiecies = filters.filter_contours(contours, hierarchy)

    # It's a good idea to simplify the contours to their convex hulls.
    simplified_contours = [cv2.convexHull(contour) for contour in filtered_contours]

    if not len(simplified_contours) == 0:
        # For now, we select "the most rectangular" contour.
        # There should be a threshold to find more license plates.
        selected_contours = [sorted(simplified_contours, key=convex_area_diff)[0]]

        corners = [find_corners(contour) for contour in selected_contours]

        # draw_contours( selected_contours, colorImage )
        draw_contours(corners, colorImage)

        # sheared_plate = perspective_warping(corners, threshholding)
        # cv2.imshow(sheared_plate)

        return True
    else:

        return False
