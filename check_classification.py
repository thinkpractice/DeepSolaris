import argparse
import csv
import cv2
from imutils.paths import list_images
import os

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input-dir", required=True, help="Input directory containing the images")
parser.add_argument("-o", "--output-file", required=True, help="Output csv file")
args = vars(parser.parse_args())

annotations = []
image_filenames = [image_filename for image_filename in list_images(args["input_dir"])]

i = 0
while True:
        image_filename = image_filenames[i]
        image = cv2.imread(image_filename)
        cv2.imshow("Image", image)
        key = cv2.waitKey(0)
        label = "ok"
        if key == ord('q'):
            break
        elif key == ord('p'):
            label = "false positive"
        elif key == ord('n'):
            label = "false negative"
        elif i > 0 and key == ord('b'):
            i -= 1
            continue
       
        object_id, _ = os.path.splitext(os.path.basename(image_filename))    
        annotations.append({"filename" : image_filename, "object_id": object_id, "classification": label})
        i += 1
        print("Annotated {} as {}".format(image_filename, label))
        print("Annotated {} out of {} images".format(i, len(image_filenames)))
        if i == len(image_filenames):
            break

print("Writing file to disk")
with open(args["output_file"], "w") as csv_file:
    csv_writer = csv.DictWriter(csv_file, delimiter=";", fieldnames=["filename", "object_id", "classification"])
    csv_writer.writeheader()         
    for annotation in annotations:
        csv_writer.writerow(annotation)
