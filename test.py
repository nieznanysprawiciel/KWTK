# -*- coding: utf-8 -*-
import cv2
import os


#print "Working directory: "
#print os.getcwd()


imagesDir = "images/"
thresholdDir = "thresh/"
filePath = imagesDir + "auto000.jpg"

images = os.listdir( imagesDir )


if not os.path.exists( thresholdDir ):
	os.makedirs( thresholdDir )
	print "Created directory: " + thresholdDir

for image in images:
	filePath = imagesDir + image

	if os.path.isfile( filePath ):
		img = cv2.imread( filePath, 0 )
		threshholding = cv2.adaptiveThreshold( img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 40 )

		#cv2.imshow( filePath, threshholding )
		print "Image thresholding result in: " + thresholdDir + image
		cv2.imwrite( thresholdDir + image, threshholding )
		
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
	else:
		print "Image doesn't exist: " + filePath