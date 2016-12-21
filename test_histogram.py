# -*- coding: utf-8 -*-
import cv2
import os
import histogram as hist
import matplotlib.pyplot as plt


print "Working directory: "
print os.getcwd()


imagesDir = "new_plates/"
# filePath = imagesDir + "a.png"

histogramDir ="histogramy/"

images = os.listdir( imagesDir )


if not os.path.exists( histogramDir ):
	os.makedirs( histogramDir )
	print "Created directory: " + histogramDir

i = -1

for image in images:
	filePath = imagesDir + image

	i = i + 1

	if os.path.isfile( filePath ):
		img = cv2.imread( filePath, cv2.cv.CV_LOAD_IMAGE_COLOR )

		greyImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		threshholding = cv2.adaptiveThreshold(greyImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 5)

		horizontal, vertical = hist.histograms(threshholding)

		fig = plt.figure(i)
		plt.plot(horizontal)
		plt.xlabel('Piksele')
		plt.ylabel('Intensywnosc')
		plt.title('Horizontal histogram ' + image)
		plt.axis()
		plt.grid(True)
		fig.savefig(histogramDir + 'horizontal' + str(i) + '.jpg', format='jpg', dpi=60)

		# histogramDir + 'histogram_' + str(i) + '.png')


		#cv2.imshow( filePath, threshholding )

		# print('Horizontal: ')
		# for i in range(len(horizontal)):
		#	print(horizontal[i])

		# print('Vertical: ')
		# for j in range(len(vertical)):
		#	print(vertical[j])
		
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
	else:
		print "Image doesn't exist: " + filePath