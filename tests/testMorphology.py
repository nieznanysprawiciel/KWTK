
# -*- coding: utf-8 -*-
import cv2
import os
import numpy as np

print "Working directory: "
print os.getcwd()


imagesDir = "thresh/"
morphologyDir = "morphology/"
filePath = imagesDir + "auto000.jpg"

images = os.listdir( imagesDir )


if not os.path.exists( morphologyDir ):
    os.makedirs( morphologyDir )
    print "Created directory: " + morphologyDir

for image in images:
    filePath = imagesDir + image

    if os.path.isfile( filePath ):
        img = cv2.imread( filePath, 0 )
        threshholding = cv2.adaptiveThreshold( img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 5 )

        new_image = img

        kernel = np.ones((2, 2), np.uint8)

        for i in range(1, 20):
            new_image = cv2.morphologyEx(new_image, cv2.MORPH_CLOSE, kernel)

        print "Image after morphology result in: " + morphologyDir + image
        cv2.imwrite( morphologyDir + image, new_image )

    else:
        print "Image doesn't exist: " + filePath
