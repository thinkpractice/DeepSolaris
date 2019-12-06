import argparse
import csv
import cv2
import os
import progressbar
from imutils.paths import list_images

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="The csv with the uuids to check")
parser.add_argument("-l", "--left_directory", required=True, help="The left directory to check for files")
parser.add_argument("-r", "--right_directory", required=True, help="The right directory to check for files")
parser.add_argument("-s", "--delimiter", default=";", help="The delimiter for the csv file")
parser.add_argument("-c", "--uuid-column", default="uuid", help="The uuid column name to use from the csv file")
parser.add_argument("-d", "--list-differences", type=bool, default=False)
args = vars(parser.parse_args())


def read_csv(filename, uuid_column):
    uuids_file = []
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=args["delimiter"])
        for line in csv_reader:
            uuids_file.append(line[uuid_column])
    return set(uuids_file)

def uuids_in_directory(directory):
    return {os.path.split(filename)[-1][:36] : filename for filename in list_images(directory)}

uuids_file = read_csv(args["input"], args["uuid_column"])
uuids_filenames_left = uuids_in_directory(args["left_directory"])
uuids_filenames_right = uuids_in_directory(args["right_directory"])

uuids_left_directory = set(uuids_filenames_left.keys())
uuids_right_directory = set(uuids_filenames_right.keys())

if uuids_file.issubset(uuids_left_directory) and uuids_file.issubset(uuid_right_directory):
    print("All uuids present in directory")
else:
    left_diff = uuids_file - uuids_left_directory
    right_diff = uuids_file - uuids_right_directory
    print("{} uuids in file, {} uuids in left directory, {} in right directory".format(len(uuids_file), len(uuids_left_directory), len(uuids_right_directory)))
    print("{} differences left, {} differences with right".format(len(left_diff), len(right_diff)))
    if args["list_differences"]:
        print("Different left uuids: {}".format(left_diff))
        print("Different right uuids: {}".format(right_diff))

left_same = uuids_file & set(uuids_left_directory)
right_same = uuids_file & set(uuids_right_directory)
same_left_right = left_same & right_same

if len(same_left_right) != len(left_same) or len(same_left_right) != len(right_same):
    print("Warning: some files are missing from the comparison")

widgets = ["Comparing images: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(maxval=len(same_left_right), widgets=widgets).start()
for i, uuid in enumerate(same_left_right):
    filename_left = uuids_filenames_left[uuid]
    filename_right = uuids_filenames_right[uuid]
    
    image_left = cv2.imread(filename_left)
    image_right = cv2.imread(filename_right)

    resize_shape = image_left.shape[:2]
    if image_left.shape[0] < image_right.shape[0] and image_left.shape[1] < image_right.shape[1]:
        resize_shape = image_right.shape[:2]

    image_left = cv2.resize(image_left, dsize=resize_shape)
    image_right = cv2.resize(image_right, dsize=resize_shape)

    cv2.imshow("Left", image_left)
    cv2.imshow("Right", image_right)

    cv2.waitKey(0)
    pbar.update(i)
pbar.finish()

cv2.destroyAllWindows()
