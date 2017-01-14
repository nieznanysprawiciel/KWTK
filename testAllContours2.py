import cv2
import os
import random
import numpy as np
import processing
import histogram as hist
import matplotlib.pyplot as plt
import characters_recognition

# print "working directory: "
# print os.getcwd()

imagesDir = "images/"
thresholdDir = "thresh/"
newPlatesDir = "new_plates/"

writeExtension = ".jpg"  # for unknown reasons sometimes python can't write image with jpg or png extension :(

imageName = "tablice_rejestracyjne.jpg"


def convex_area_diff(contour):
    xks = [point[0][0] for point in contour]
    yks = [point[0][1] for point in contour]

    rectangle_area = (max(xks) - min(xks)) * (max(yks) - min(yks))
    area = cv2.contourArea(contour)

    return float((rectangle_area - area)) / rectangle_area


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# delkaracja funkcji glownej (przekazanie sciezki do wybranego zdjecia,
# macierzy pikseli wybranego zdjecia, parametru nr 1 oraz nr 2
# jako argumentow funkcji)
def plate_recog(_path, _colorImage, threshold, idx_threshold):
    print "Recognition started, threshold = {}, idx_threshold = {}".format(threshold, idx_threshold)

    if not os.path.exists(newPlatesDir):
        os.makedirs(newPlatesDir)
        print ("Created directory: " + newPlatesDir)

    # initialize of random numbers
    random.seed()

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # usuniecie petli for - uzytkownik wybiera tylko jedno zdjecie

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # pobranie sciezki wybranego zdjecia
    filePath = _path
    path_list = filePath.split("/")
    sz = len(path_list) - 1
    image = path_list[sz]

    # deklaracja listy koncowych wynikow
    results = {}
    results[3] = False

    if os.path.isfile(filePath):

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # obraz jest wczytywany juz w GUI, tutaj przekazujemy jedynie macierz pikseli

        processed_image = processing.process_area_only2(_colorImage)

        if processed_image is not None:

            pre, ext = os.path.splitext(image)
            image = pre + writeExtension
            resultFile = newPlatesDir + image

            cv2.imwrite(resultFile, processed_image)
            print ("Segmented image result in: ") + resultFile

            ### Letters segmentation
            greyImage = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
            threshholding_letters = cv2.adaptiveThreshold(greyImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                          cv2.THRESH_BINARY, 15, 5)
            segments = hist.histogram_segmentation(threshholding_letters, threshold, idx_threshold)

            height = processed_image.shape[0]

            license_plate = ""
            probable_characters = []

            k = 0
            for segment in segments:

                # 1 Cropping segments from original images
                crop_img = processed_image[0:height, segment[0]:segment[1]]
                cv2.imwrite(newPlatesDir + pre + "_segmented_" + str(k) + writeExtension, crop_img)

                # 2 Creating histograms of cropped images
                greyImage = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
                threshholding_crop = cv2.adaptiveThreshold(greyImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                           cv2.THRESH_BINARY,
                                                           15, 5)
                horizontal_crop, vertical_crop = hist.histograms(threshholding_crop)

                # 3 Drawing histograms - turned off because it interferes with PyTk GUI and causes bugs in open file dialog
                # saveFileHorizontal = str(newPlatesDir + pre + "_segmented_" + str(k) + "horizontal" + writeExtension)
                # saveFileVertical = str(newPlatesDir + pre + "_segmented_" + str(k) + "vertical" + writeExtension)
                # processing.drawing_segments_histograms(horizontal_crop, vertical_crop, saveFileHorizontal, saveFileVertical)

                # 4 Drawing a rectangles in the picture
                cv2.rectangle(processed_image, (segment[0], 0), (segment[1], height - 1), (255, 0, 0), 1)

                # 5 Characters recognition
                grey_crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
                binary_crop_img = cv2.adaptiveThreshold(
                    grey_crop_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 5)
                binary_crop_img = cv2.cvtColor(binary_crop_img, cv2.COLOR_GRAY2BGR)

                cv2.imwrite(newPlatesDir + pre + "_segmented_" + str(k) + writeExtension, binary_crop_img)

                possibilities = characters_recognition.find_matching_characters(binary_crop_img)
                best_probability = possibilities[0][1]

                if best_probability > 0.15:
                    license_plate += possibilities[0][0].upper()
                    probable_characters += [possibilities[0:5]]

                    # 2 Drawing a rectangles in the picture
                    cv2.rectangle(processed_image, (segment[0], 0), (segment[1], height - 1), (255, 0, 0), 1)

                k += 1

            print("Recognized " + license_plate)
            print("Possibilities:")
            print(probable_characters)

            resultFile = newPlatesDir + pre + "_segmented"
            cv2.imwrite(resultFile + writeExtension, processed_image)
            # else:
            # raise Exception("No license plate found!")
            print('Segments')
            print(segments)

    else:
        print ("Image doesn't exist: " + filePath)

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # przypisanie wyikow do listy
    # wyjatek - gdy brak zwroconych wynikow (kiedy algorytm nie dal rady)
    try:
        # przypisanie wynikow - odczytanych numerow (license_plate),
        # pozostalych znakow (probable_characters) oraz sciezki do analizowanego
        # fragmentu zdjecia (resultFile) do listy results
        results[0] = license_plate
        results[1] = probable_characters
        results[2] = resultFile
    except(UnboundLocalError):
        results[3] = True
    return results
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


