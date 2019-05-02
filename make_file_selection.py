import json
import argparse
import os
import shutil


def copy_images(annotation_filename, output_dir):
    with open(annotation_filename) as json_file:
        annotation_dict = json.load(json_file)
        image_dicts = annotation_dict["images"]

        images = []
        for image_dict in image_dicts:
            filename = image_dict["filename"]
            shutil.copy(filename, output_dir)


def copy_all_images(annotation_filename, output_dir, merge_filename):
    copy_images(annotation_filename, output_dir)
    copy_images(merge_filename, output_dir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="The input file with the annotations")
    parser.add_argument("-o", "--output", required=True, help="The output folder with the images to write")
    parser.add_argument("-m", "--merge", default=None, help="The annotation file to merge with the first")
    args = vars(parser.parse_args())
    write_images(args["input"], args["output"], args["merge"])


if __name__ == "__main__":
    main()