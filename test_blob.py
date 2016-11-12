# -*- coding: utf-8 -*-
# Standard imports
import cv2
import numpy as np
import os


thresholdDir = "thresh/"
blobDir = "blob/"
filePath = thresholdDir + "auto000.jpg"

images = os.listdir(thresholdDir)

if not os.path.exists(blobDir):
    os.makedirs(blobDir)
    print "Created directory: " + blobDir

for image in images:
    filePath = thresholdDir + image

    if os.path.isfile(filePath):
        # Read image
        im = cv2.imread(filePath, cv2.IMREAD_GRAYSCALE)

        # Set up the detector with default parameters.
        detector = cv2.SimpleBlobDetector()

        # Detect blobs.
        keypoints = detector.detect(im)

        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # Show keypoints
        # cv2.imshow("Keypoints", im_with_keypoints)


        cv2.imwrite(blobDir + image, im_with_keypoints )
        # cv2.waitKey(0)

    else:
        print "Image doesn't exist: " + filePath









