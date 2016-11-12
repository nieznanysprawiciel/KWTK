# -*- coding: utf-8 -*-
import cv2
import os

#print "Working directory: "
#print os.getcwd()


imagesDir = "images/"
histDir = "hist/"
medianDir = "median/"
filePath = imagesDir + "auto000.jpg"

images = os.listdir( imagesDir )


# Equalized histogram and added gaussian blur
if not os.path.exists( histDir ):
	os.makedirs( histDir )
	print "Created directory: " + histDir

if not os.path.exists( medianDir ):
	os.makedirs( medianDir )
	print "Created directory: " + medianDir

for image in images:
	filePath = imagesDir + image

	if os.path.isfile( filePath ):
		img = cv2.imread( filePath, 0 )
		# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		eq_hist = cv2.equalizeHist(img)

		#cv2.imshow( filePath, threshholding )
		print "Image equalizeHist result in: " + histDir + image
		cv2.imwrite( histDir + image, eq_hist )

		img2 = cv2.GaussianBlur(eq_hist, (6, 6), 0)
		print "Image GaussianBlur result in: " + medianDir + image
		cv2.imwrite(medianDir + image, eq_hist)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
	else:
		print "Image doesn't exist: " + filePath


