import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--left", required=True, help="The first annotation file to use")
parser.add_argument("-r", "--right", required=True, help="The second annotation file to use")
parser.add_argument("-o", "--output", required=True, help="The output file to write")
args = vars(parser.parse_args())

with open(args["left"]) as left_file:
    left_json = json.load(left_file)
    print("Read {} rows from left file".format(len(left_json)))

with open(args["right"]) as right_file:
    right_json = json.load(right_file)
    print("Read {} rows from right file".format(len(right_json)))

with open(args["output"], "w") as output_file:
    merged_json = {"current_page_index" : left_json["current_page_index"], "images": left_json["images"] + right_json["images"]}
    json.dump(merged_json, output_file)
    print("Wrote {} rows to output file".format(len(merged_json)))
