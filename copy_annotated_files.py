import argparse
import json
import os
import shutil
import progressbar

def load_annotations(filename):
    with open(filename, "r") as json_file:
        annotations = json.load(json_file)
        classes = annotations.get("classes", {
            False: "no_panels",
            True: "panels"
        })
        return classes, annotations["images"]


def create_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def copy_annotated_files(input_dataset, annotations, classes, output_dir):
    widgets = ["Extracting Features: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
    pbar = progressbar.ProgressBar(maxval=len(annotations), widgets=widgets).start()
    for i, annotation in enumerate(annotations):
        annotation_class = classes.get(annotation["annotation"], None)
        if not annotation_class:
            continue
        src_file = os.path.join(input_dataset, os.path.basename(annotations["filename"]))
        class_dir = os.path.join(output_dir, annotation_class)
        shutil.copy2(src_file, class_dir)

        pbar.update(i)
    pbar.finish()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Input json file with the annotations")
    parser.add_argument("-d", "--dataset", required=True, help="The dataset to copy images from")
    parser.add_argument("-o", "--output", required=True, help="The output folder to copy the images to")
    args = vars(parser.parse_args())

    classes, annotations = load_annotations(args["input"])
    create_if_not_exists(args["output"])
    for annotation_class in classes:
        create_if_not_exists(os.path.join(args["output"], annotation_class))

    copy_annotated_files(args["dataset"], annotations, classes, args["output"])


if __name__ == "__main__":
    main()

