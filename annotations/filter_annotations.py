import argparse
import csv


def keep_row_dkn(row):
    return row["label"] != -1

def keep_row(row, method):
    return keep_row_dkn(row)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="The input csv to filter")
parser.add_argument("-o", "--output", required=True, help="The filtered output csv")
parser.add_argument("-m", "--method", default="dkn", help="The method for filtering")
args = vars(parser.parse_args())

num_rows_read = 0
num_rows_written = 0
with open(args["input"]) as csv_input:
    csv_reader = csv.DictReader(csv_input, delimiter=";")
    with open(args["output"], "w") as csv_output:
        csv_writer = csv.DictWriter(csv_output, delimiter=";", fieldnames=["uuid", "label"])
        csv_writer.writeheader()

        for row in csv_reader:
            num_rows_read += 1
            if not keep_row(row, args["method"]):
                continue
            csv_writer.writerow({"uuid": row["uuid"], "label": row["label"]})
            num_rows_written += 1

print("Filtered rows, read: {} rows, wrote: {} rows".format(num_rows_read, num_rows_written))

