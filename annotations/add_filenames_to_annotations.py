import argparse
import csv
import os


def get_filenames(paths_filename):
    with open(paths_filename) as paths_csv:
        csv_reader = csv.DictReader(paths_csv, delimiter=";")
        return {row["dataset_name"]: row for row in csv_reader}


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="The input csv file containing the annotations")
parser.add_argument("-p", "--paths", required=True, help="The csv file containing the paths")
parser.add_argument("-o", "--output", required=True, help="The output csv file")
args = vars(parser.parse_args())

filenames_dict = get_filenames(args["paths"])

num_rows_read = 0
num_rows_written = 0
with open(args["input"]) as csv_input:
    csv_reader = csv.DictReader(csv_input, delimiter=";")
    with open(args["output"], "w") as csv_output:
        csv_writer = csv.DictWriter(csv_output, fieldnames=csv_reader.fieldnames + ["filename"], delimiter=";")
        csv_writer.writeheader()
        for row in csv_reader:
            num_rows_read += 1

            dataset = row["name"]
            dataset_row = filenames_dict.get(dataset, None)
            if not dataset_row:
                continue

            dataset_path = dataset_row.get("path", None)
            extension = dataset_row.get("extension", None)
            if not dataset_path or not extension:
                continue

            filename = os.path.join(dataset_path, "{uuid}{extension}".format(uuid=row["uuid"], extension=extension))
            row["filename"] = filename
            csv_writer.writerow(row)
            num_rows_written += 1

print("Read: {} rows and written: {} rows".format(num_rows_read, num_rows_written))

