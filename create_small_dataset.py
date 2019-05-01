from ProjectPaths import ProjectPaths
import numpy as np
import os
import cv2


heerlen_images_filename = os.path.join(ProjectPaths.instance().image_dir, "deepsolaris_heerlen.npy")
heerlen_labels_filename = os.path.join(ProjectPaths.instance().image_dir, "deepsolaris_heerlen_labels.npy")

heerlen_images = np.load(heerlen_images_filename)
heerlen_labels = np.load(heerlen_labels_filename)

import cv2

num_positives = 0
num_negatives = 0
for i, (label, image) in enumerate(zip(heerlen_labels, heerlen_images)):
    if num_positives < 10 and label == 1:
        cv2.imwrite("positive_{}.png".format(num_positives), image)
        num_positives += 1
    if num_negatives < 10 and label == 0:
        cv2.imwrite("negative_{}.png".format(num_negatives), image)
        num_negatives += 1
