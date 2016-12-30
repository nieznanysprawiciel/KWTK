import cv2
import os
import random
import numpy as np
import processing
import histogram as hist
import matplotlib.pyplot as plt

#print "working directory: "
#print os.getcwd()


def convex_area_diff (contour):

    xks = [point[0][0] for point in contour]
    yks = [point[0][1] for point in contour]

    rectangle_area = (max(xks) - min(xks)) * (max(yks) - min(yks))
    area = cv2.contourArea(contour)

    return float((rectangle_area - area))/rectangle_area


######################



imagesDir = "images/"
thresholdDir = "thresh/"
newPlatesDir = "new_plates/"

writeExtension = ".jpg"        # for unknown reasons sometimes python can't write image with jpg or png extension :(

imageName = "auto000.jpg"
filePath = imagesDir + imageName

if not os.path.exists( newPlatesDir ):
    os.makedirs( newPlatesDir)
    print "Created directory: " + newPlatesDir

# initialize of random numbers
random.seed()

imageFiles = os.listdir( imagesDir )

for image in imageFiles:

    filePath = imagesDir + image

    if os.path.isfile( filePath ):   
        colorImage = cv2.imread( filePath, cv2.cv.CV_LOAD_IMAGE_COLOR )

        processed_image = processing.process_area_only2( colorImage )

        #if processing.process( colorImage ):
        if processed_image is not None:
            #cv2.imshow( filePath, colorImage )

            pre, ext = os.path.splitext( image )
            image = pre + writeExtension
            resultFile = newPlatesDir + image

            cv2.imwrite( resultFile, processed_image )
            print "Segmented image result in: " + resultFile
            
            ### Letters segmentation
            greyImage = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
            threshholding_letters = cv2.adaptiveThreshold( greyImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 5 )
            segments = hist.histogram_segmentation( threshholding_letters, 0.09, 6 )


            height = processed_image.shape[ 0 ]

            k = 0
            for segment in segments:

                #1 Cropping segments from original images
                crop_img = processed_image[0:height, segment[0]:segment[1]]
                cv2.imwrite(newPlatesDir + pre + "_segmented_" + str(k) + writeExtension, crop_img )

                #2 Creating histograms of cropped images
                greyImage = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
                threshholding_crop = cv2.adaptiveThreshold(greyImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
                                                      15, 5)
                horizontal_crop, vertical_crop = hist.histograms(threshholding_crop)

                #3 Drawing histograms
                saveFileHorizontal = str(newPlatesDir + pre + "_segmented_" + str(k) + "horizontal" + writeExtension)
                saveFileVertical = str(newPlatesDir + pre + "_segmented_" + str(k) + "vertical" + writeExtension)
                processing.drawing_segments_histograms(horizontal_crop, vertical_crop, saveFileHorizontal, saveFileVertical)


                #4 Drawing a rectangles in the picture
                cv2.rectangle(processed_image, (segment[0], 0), (segment[1], height - 1), (255, 0, 0), 1)

                k += 1

            resultFile = newPlatesDir + pre + "_segmented"
            cv2.imwrite( resultFile + writeExtension, processed_image )
        #else:
            #raise Exception("No license plate found!")
            print('Segments')
            print(segments)

    else:
        print "Image doesn't exist: " + filePath

cv2.waitKey(0)
cv2.destroyAllWindows()
        
#
