from DirectoryFilter import DirectoryFilter
import os
import csv
import argparse


def read_pv_file(filename):
    with open(filename) as csvFile:
        csv_reader = csv.DictReader(csvFile)
        return [row for row in csv_reader]


def locations_per_year(pv_locations):
    years = {location["year_in_use"] for location in pv_locations}
    return {year: [row for row in pv_locations if int(row["year_in_use"]) <= year] for year in years}


def extract_uuid(path):
    filename = os.path.basename(path)
    return filename[:36]


def uuids_from_filenames(filenames):
    return sorted(list({extract_uuid(filename) for filename in filenames}))


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
    parser.add_argument("-i", "--input_file", required=True, help="The csv file with pv panel locations")
    parser.add_argument("-o", "--output_file", required=True, help="The json file with annotations")
    parser.add_argument("-d", "--image_dir", required=True, help="The directory with the image files")
    parser.add_argument("-t", "--image_type", required=False, default="rgb", help="The type of files (rgb, ir, etc.)")
    parser.add_argument("-w", "--width", required=False, default=75, help="The width of each image")
    parser.add_argument("-h", "--height", required=False, default=75, help="The height of each image")
    parser.add_argument("-c", "--current_index", required=False, default=0,
                        help="The current page index to start annotating")

    args = vars(parser.parse_args())
    pv_locations = read_pv_file(args["pv_file"])
    locations = locations_per_year(pv_locations)

    directory_filter = DirectoryFilter(root_path=args["image_dir"])
    images = directory_filter.rgb.images.paths

    