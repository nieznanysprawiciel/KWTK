# -*- coding: utf-8 -*-
import cv2
import os
import histogram as hist
import matplotlib.pyplot as plt


print "Working directory: "
print os.getcwd()


imagesDir = "wzorce/"
# filePath = imagesDir + "a.png"

histogramDir ="histogramy_wzorcow/"

images = os.listdir( imagesDir )


if not os.path.exists( histogramDir ):
	os.makedirs( histogramDir )
	print "Created directory: " + histogramDir



for image in images:
	filePath = imagesDir + image


	if os.path.isfile( filePath ):

		pre, ext = os.path.splitext(image)

		img = cv2.imread( filePath, cv2.cv.CV_LOAD_IMAGE_COLOR )

		greyImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		threshholding = cv2.adaptiveThreshold(greyImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 5)

		horizontal, vertical = hist.histograms(threshholding)

		print("horizontal len: " + str(len(horizontal)))
		print("vertical len: " + str(len(vertical)))

		fig = plt.figure()
		plt.plot(horizontal)
		plt.xlabel('Piksele')
		plt.ylabel('Intensywnosc')
		plt.title('Horizontal histogram ' + image)
		plt.axis()
		plt.grid(True)
		fig.savefig(histogramDir + pre + '_horizontal' + '.jpg', format='jpg', dpi=60)

		fig = plt.figure()
		plt.plot(vertical)
		plt.xlabel('Piksele')
		plt.ylabel('Intensywnosc')
		plt.title('Vertical histogram ' + image)
		plt.axis()
		plt.grid(True)
		fig.savefig(histogramDir + pre + '_vertical' + '.jpg', format='jpg', dpi=60)

	else:
		print "Image doesn't exist: " + filePath