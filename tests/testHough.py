import cv2
import os
import numpy as np

#print "working directory: "
#print os.getcwd()


imagesDir = "images/"
thresholdDir = "thresh/"
contoursDir = "contours/"
houghDir = "hough/"


writeExtension = ".jpg"		# for unknown reasons sometimes python can't write image with jpg or png extension :(

imageName = "auto000.jpg"
filePath = imagesDir + imageName

if not os.path.exists( houghDir ):
	os.makedirs( houghDir )
	print "Created directory: " + houghDir


if os.path.isfile( filePath ):
	srcImage = cv2.imread( filePath, 0 )
	colorImage = cv2.imread( filePath, cv2.cv.CV_LOAD_IMAGE_COLOR )
	#threshholding = cv2.adaptiveThreshold( srcImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2 )
	threshholding = cv2.Canny(srcImage,50,150,apertureSize = 3)
	
	lines = cv2.HoughLines( threshholding, 1, np.pi/180, 150 )
	
	# print to image
	for rho,theta in lines[0]:
		a = np.cos(theta)
		b = np.sin(theta)
		x0 = a*rho
		y0 = b*rho
		x1 = int(x0 + 1000*(-b))
		y1 = int(y0 + 1000*(a))
		x2 = int(x0 - 1000*(-b))
		y2 = int(y0 - 1000*(a))

		cv2.line( colorImage, (x1,y1), (x2,y2), (0,0,255), 2 )
	
	cv2.imshow( filePath, colorImage )
	
	pre, ext = os.path.splitext( imageName )
	imageName = pre + writeExtension
	resultFile = houghDir + imageName
	
	cv2.imwrite( resultFile, colorImage )
	print "Hough transform result image in: " + resultFile
	
else:
	print "Image doesn't exist: " + filePath