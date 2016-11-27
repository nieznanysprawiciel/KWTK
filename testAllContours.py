import cv2
import os
import random
import numpy as np

#print "working directory: "
#print os.getcwd()


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


def rectangle_similarity ( contour ):
    """
    The smaller the value the more rectangular.
    To make this metric work well, the contour should be convex.
    """
    xks = [point[0][0] for point in contour]
    yks = [point[0][1] for point in contour]

    dist_xks = [min(x - min(xks), max(xks) - x) for x in xks]
    dist_yks = [min(y - min(yks), max(yks) - y) for y in yks]

    return (sum(dist_xks) + sum(dist_yks)) / float(len(contour))

	
# http://stackoverflow.com/questions/21030391/how-to-normalize-array-numpy
def normalize(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)

def top_left_compare ( point ):
	return point[ 0 ][ 0 ] + point[ 0 ][ 1 ]
	
def top_right_compare( point ):
	return point[ 0 ][ 0 ] - point[ 0 ][ 1 ]

def dot_metric ( edge_vectors, begin_points, pixel ):
	cur_dot = 1
	for i in range(0, 3):
		pixel_vec = normalize( pixel[ 0 ] - begin_points[ i ] )
		dot = np.dot( edge_vectors[ i ], np.transpose( pixel_vec ) )
		if dot > 0:
			cur_dot = min( dot, cur_dot )
		
	return cur_dot
	
def rectangle_dot_similarity ( contour ):
	"""
	Compute dot product between edge vectors and each contour point
	"""
	
	top_left = min( contour, key = top_left_compare )
	top_right = max( contour, key = top_right_compare )
	bottom_right = max( contour, key = top_left_compare )
	bottom_left = min( contour, key = top_right_compare )
	
	
	#begin_points = [ top_left, bottom_left, top_left, top_right ]
	
	edge_vectors = [ top_right - top_left, bottom_right - bottom_left, bottom_left - top_left, bottom_right - top_right ]
	
	norms = [ np.linalg.norm( edge_vectors[ 0 ] ), np.linalg.norm( edge_vectors[ 1 ] ), np.linalg.norm( edge_vectors[ 2 ] ), np.linalg.norm( edge_vectors[ 3 ] ) ]
	
	norm_diff1 = 1.0 - abs( norms[ 0 ] - norms[ 1 ] ) / ( 2 * ( norms[ 0 ] + norms[ 1 ] ) )
	norm_diff2 = 1.0 - abs( norms[ 2 ] - norms[ 3 ] ) / ( 2 * ( norms[ 2 ] + norms[ 3 ] ) )
	
	edge_vectors = [ normalize( edge_vector ) for edge_vector in edge_vectors ]
	
	dot1 = np.dot( edge_vectors[ 0 ], np.transpose( edge_vectors[ 1 ] ) )
	dot2 = np.dot( edge_vectors[ 2 ], np.transpose( edge_vectors[ 3 ] ) )
	
	#dots = [ dot_metric( edge_vectors, begin_points, pixel ) for pixel in contours ]
	
	return (dot1 + dot2 + norm_diff1 + norm_diff2 ) / 4
	
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
			selected_contours = [sorted(simplified_contours, key=rectangle_dot_similarity)[0]]

			for contour in simplified_contours:
				print(rectangle_dot_similarity(contour))

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
