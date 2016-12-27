import os

import cv2

pattern_directory = "wzorce"
pattern_files = os.listdir(pattern_directory)

patterns = {}

for pattern_file in pattern_files:
    full_path = os.path.join(pattern_directory, pattern_file)
    if os.path.isfile(full_path):
        character, _ = os.path.splitext(os.path.basename(pattern_file))
        patterns[character] = cv2.imread(full_path)


def calculate_correlation_metric(image, pattern):
    pattern_size = (pattern.shape[1], pattern.shape[0])
    resized_image = cv2.resize(image, pattern_size)
    return cv2.matchTemplate(resized_image, pattern, cv2.TM_CCOEFF_NORMED)[0][0]


def find_matching_characters(image):
    metrics = {character: calculate_correlation_metric(image, pattern) for (character, pattern) in patterns.iteritems()}
    return sorted(metrics.items(), key=lambda metric_entry: -metric_entry[1])
