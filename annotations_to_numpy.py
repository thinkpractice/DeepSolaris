import numpy as np
import cv2
import json
import argparse
import os


def load_images(annotation_filename):
    with open(annotation_filename) as json_file:
        annotation_dict = json.load(json_file)
        image_dicts = annotation_dict["images"]

        labels = []
        images = []
        for image_dict in image_dicts:
            labels.append(1 if image_dict["annotation"] else 0)
            filename = image_dict["filename"]
            images.append(cv2.imread(filename))
        return labels, images


def label_filename(output_filename):
    path, ext = os.path.splitext(output_filename)
    return "{}_labels.{}".format(path, ext)


def write_images(annotation_filename, output_filename, merge_filename):
    labels, images = load_images(annotation_filename)
    if merge_filename:
        merge_labels, merge_images = load_images(merge_filename)
        labels.append(merge_labels)
        images.append(merge_images)

    np.save(output_filename, images)
    np.save(label_filename(output_filename), labels)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="The input file with the annotations")
    parser.add_argument("-o", "--output", required=True, help="The numpy file with the images to write")
    parser.add_argument("-m", "--merge", default=None, help="The annotation file to merge with the first")
    args = vars(parser.parse_args())
    write_images(args["input"], args["output"], args["merge"])


if __name__ == "__main__":
    main()
