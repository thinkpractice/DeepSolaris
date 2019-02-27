import argparse
import json
import os


def write_annotations(annotations, output_filename):
    if os.path.exists(output_filename):
        with open(output_filename, "r") as json_file:
            old_annotation_dict = json.load(json_file)
            old_annotations = old_annotation_dict["images"]
            old_annotations.append(annotations)
            annotations = old_annotations

    with open(output_filename, "w") as output_file:
        json.dump({
            "current_page_index": 0,
            "images": annotations
        }, output_file)


def split_annotations(input_filename, positives_filename, negatives_filename):
    with open(input_filename, "r") as input_file:
        annotations_dict = json.load(input_file)
        image_annotations = annotations_dict["images"]
        write_annotations([image_annotation
                           for image_annotation in image_annotations
                           if image_annotation["annotation"]], positives_filename)
        write_annotations([image_annotation
                           for image_annotation in image_annotations
                           if not image_annotation["annotation"]], negatives_filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="The source annotation file that has to be split")
    parser.add_argument("-p", "--positives_file", required=True, help="The filename for the positive annotations")
    parser.add_argument("-n", "--negatives_file", required=True, help="The filename for the negative annotations")
    args = vars(parser.parse_args())
    split_annotations(args["input"], args["positives_file"], args["negatives_file"])


if __name__ == "__main__":
    main()
