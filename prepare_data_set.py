from DirectoryFilter import DirectoryFilter
import os
import csv
import argparse
import json


def read_pv_file(filename):
    with open(filename) as csvFile:
        csv_reader = csv.DictReader(csvFile)
        return [row for row in csv_reader]


def extract_uuid(path):
    filename = os.path.basename(path)
    return filename[:36]


def uuids_from_filenames(filenames):
    return sorted(list({extract_uuid(filename) for filename in filenames}))


def filter_files(image_paths, filter_file):
    filter_rows = read_pv_file(filter_file)
    filter_uuids = {row["uuid"] for row in filter_rows}
    return [image_path for image_path in image_paths if extract_uuid(image_path) in filter_uuids]


def dict_for_path(index, image_path, width, height, annotation):
    return {"id": index,
            "width": width,
            "height": height,
            "annotation": annotation,
            "prediction": 1,
            "filename": image_path
            }


def create_json_dict(image_paths, width, height, annotation=True, current_page_index=0):
    return {"current_page_index": current_page_index,
            "images": [dict_for_path(i, image_path, width, height, annotation)
                       for i, image_path in enumerate(image_paths)]
            }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image_dir", required=True, help="The directory with the image files")
    parser.add_argument("-o", "--output_file", required=True, help="The json file with annotations")
    parser.add_argument("-f", "--filter_file", help="The csv file with pv panel locations")
    parser.add_argument("-t", "--image_type", default="rgb", help="The type of files (rgb, ir, etc.)")
    parser.add_argument("-c", "--width",  default=75, type=int, help="The width of each image")
    parser.add_argument("-r", "--height",  default=75, type=int, help="The height of each image")
    parser.add_argument("-a", "--annotation", default=True, type=bool, help="The default annotation to give all images")
    parser.add_argument("-b", "--current_index", default=0,
                        help="The current page index to start annotating")

    args = vars(parser.parse_args())

    directory_filter = DirectoryFilter(root_path=args["image_dir"])
    image_paths = directory_filter.rgb.images.paths
    filter_file = args.get("filter_file", None)
    if filter_file:
        image_paths = filter_files(image_paths, filter_file)

    annotation_dict = create_json_dict(image_paths, args["width"], args["height"], args["annotation"], args["current_index"])
    with open(args["output_file"], "w") as json_file:
        json.dump(annotation_dict, json_file, indent=4, sort_keys=True)

if __name__ == "__main__":
    main()

