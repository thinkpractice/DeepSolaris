import argparse
import json
import csv
import os

def get_uuid(path):
    return os.path.basename(path)[:36]

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="The csv file to join the annotations too")
parser.add_argument("-a", "--annotations", required=True, help="The json file withe annotations")
parser.add_argument("-o", "--output", required=True, help="The output csv file")
args = vars(parser.parse_args())

with open(args["input"]) as input_csv:
    csv_reader = csv.DictReader(input_csv, delimiter=",")
    csv_rows = {row["uuid"] : row for row in csv_reader}
    print("Number of image rows read from csv {}".format(len(csv_rows)))

with open(args["annotations"]) as annotation_json:
    annotations = json.load(annotation_json)
    annotation_rows = {get_uuid(annotation["filename"]) : annotation for annotation in annotations["images"]}
    print("Number of annotations read from json {}".format(len(annotations["images"])))

with open(args["output"], "w") as output_csv:
    csv_writer = csv.DictWriter(output_csv, delimiter=";", fieldnames=list(csv_rows.keys()) + list(annotations.keys()))
    number_of_rows_written = 0
    csv_writer.writeheader()
    for uuid, row in csv_rows.items():
        if uuid not in annotation_rows.keys():
            continue
        annotation_row = annotation_rows[uuid]    
        new_row = {**row, **annotation_row}    
        csv_writer.writerow(new_row)
        number_of_rows_written += 1
    print("Number of rows merged: {}".format(number_of_rows_written))


