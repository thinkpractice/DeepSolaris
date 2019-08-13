import argparse
import csv


def max_label_for_row(row):
    num_positives = row["positives"]
    num_negatives = row["negatives"]
    num_dkn = row["dkn"]
    if num_positives > num_negatives and num_positives >= num_dkn:
        return 1
    elif num_negatives > num_positives and num_negatives >= num_dkn:
        return 0
    return -1


def label_for_row(row, method):
    return max_label_for_row(row)


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="The input file containing the raw annotations")
parser.add_argument("-o", "--output", required=True, help="The output file containing the labels")
parser.add_argument("-m", "--method", default="max", help="The method to use to label the annotations")
args = vars(parser.parse_args())

num_rows_written = 0
with open(args["input"]) as csv_input:
    csv_reader = csv.DictReader(csv_input, delimiter=";")
    with open(args["output"], "w") as csv_output:
        csv_writer = csv.DictWriter(csv_output, delimiter=";", fieldnames=csv_reader.fieldnames + ["label"])
        csv_writer.writeheader()
        for row in csv_reader:
            label = label_for_row(row, args["method"])
            row["label"] = label
            csv_writer.writerow(row)
            num_rows_written += 1

print("Labeled {} rows".format(num_rows_written))

