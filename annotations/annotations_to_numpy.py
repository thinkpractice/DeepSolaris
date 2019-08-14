import argparse
import csv
import numpy as np
import cv2
import os
import progressbar
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="The input csv with the annotations and filenames of the annotations")
parser.add_argument("-o", "--output", required=True, help="The output directory to contain the numpy images")
parser.add_argument("-t", "--target-size", default=(187,187), nargs='+', type=int, help="The target size for the network input")
args = vars(parser.parse_args())

target_size = tuple(args["target_size"])

with open(args["input"]) as csv_input:
    csv_reader = csv.DictReader(csv_input, delimiter=";")
    image_filenames = defaultdict(list)
    image_labels = defaultdict(list)
    for row in csv_reader:
        parent_dataset_name = row["parent_dataset"]      
        image_filenames[parent_dataset_name].append(row["filename"])
        image_labels[parent_dataset_name].append(row["label"])

for dataset_name, image_paths in image_filenames.items():
    widgets = ["Writing images for {} dataset: ".format(dataset_name), progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
    pbar = progressbar.ProgressBar(maxval=len(image_paths), widgets=widgets).start()
   
    images = []
    for i, image_path in enumerate(image_paths):
        image = cv2.imread(image_path)
        image = cv2.resize(image, target_size)
        images.append(image)
        pbar.update(i)
    pbar.finish()    

    np_images = np.array(images)
    np.save(os.path.join(args["output"], "{}.npy".format(dataset_name)), np_images)
    np_labels = np.array(image_labels[dataset_name])
    np.save(os.path.join(args["output"], "{}_labels.npy".format(dataset_name)), np_labels)

