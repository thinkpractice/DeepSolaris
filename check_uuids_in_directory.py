import argparse
import csv
import os
from imutils.paths import list_images

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="The csv with the uuids to check")
parser.add_argument("-d", "--directory", required=True, help="The directory to check for files")
parser.add_argument("-s", "--delimiter", default=";", help="The delimiter for the csv file")
parser.add_argument("-c", "--uuid-column", default="uuid", help="The uuid column name to use from the csv file")
parser.add_argument("-l", "--list-differences", type=bool, default=False)
args = vars(parser.parse_args())

uuids_file = []
with open(args["input"]) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=args["delimiter"])
    for line in csv_reader:
        uuid_column = args["uuid_column"]
        uuids_file.append(line[uuid_column])
uuids_file = set(uuids_file)

uuids_directory = [os.path.split(filename)[-1][:36] for filename in list_images(args["directory"])]
uuids_directory = set(uuids_directory)

if uuids_file.issubset(uuids_directory):
    print("All uuids present in directory")
else:
    diff = uuids_file - uuids_directory
    intersection = uuids_file & uuids_directory
    print("{} uuids in file, {} uuids in directory".format(len(uuids_file), len(uuids_directory)))
    print("{} differences, {} common".format(len(diff), len(intersection)))
    if args["list_differences"]:
        print("Different uuids: {}".format(diff))


