import cv2
import os
import random

#print "working directory: "
#print os.getcwd()


imagesDir = "images/"
thresholdDir = "thresh/"
contoursDir = "contours/"

writeExtension = ".jpg"		# for unknown reasons sometimes python can't write image with jpg or png extension :(

imageName = "auto000.jpg"
filePath = imagesDir + imageName

if not os.path.exists( contoursDir ):
    os.makedirs( contoursDir )
	print "Created directory: " + contoursDir

random.seed()

if os.path.isfile( filePath ):
	srcImage = cv2.imread( filePath, 0 )
	colorImage = cv2.imread( filePath, cv2.cv.CV_LOAD_IMAGE_COLOR )
	threshholding = cv2.adaptiveThreshold( srcImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2 )
	
	#cv2.imshow( "src", srcImage )
	#cv2.imshow( "copy", colorImage )
	
	contours, hierarchy = cv2.findContours( threshholding, cv2.cv.CV_RETR_LIST , cv2.cv.CV_CHAIN_APPROX_NONE )
	
	for idx in range( 0, len( contours ) ):
		R = random.randint( 0, 255 )
		G = random.randint( 0, 255 )
		B = random.randint( 0, 255 )
		
		cv2.drawContours( colorImage, contours, idx, ( R, G, B ), cv2.cv.CV_FILLED )
	
	cv2.imshow( filePath, colorImage )
	
	pre, ext = os.path.splitext( imageName )
	imageName = pre + writeExtension
	resultFile = contoursDir + imageName
	
	cv2.imwrite( resultFile, colorImage )
	print "Segmented image result in: " + resultFile
	
	cv2.waitKey(0)
	cv2.destroyAllWindows()
else:
	print "Image doesn't exist: " + filePath
