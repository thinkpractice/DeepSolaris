import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="Input csv file")
parser.add_argument("-j", "--join", required=True, help="File to join")
parser.add_argument("-o", "--output", required=True, help="Output file")
parser.add_argument("-c", "--column_name", required=True, help="Column name to join on")
args = vars(parser.parse_args())

column_name = args["column_name"]
with open(args["join"]) as join_file:
    join_csv = csv.DictReader(join_file, delimiter=";")
    join_records = {row[column_name] : row for row in join_csv}

joined_rows = []
with open(args["input"]) as input_file:
    input_csv = csv.DictReader(input_file, delimiter=";")
    for row in input_csv:
        if row["classification"] == "ok":
            continue

        object_id = row[column_name]
        if object_id in join_records.keys():
            add_row = join_records[object_id]
            for key, value in add_row.items():
                if key != column_name:
                    row[key] = value
            joined_rows.append(row)


with open(args["output"], "w") as output_file:
    csv_writer = csv.DictWriter(output_file, delimiter=";", fieldnames=joined_rows[0].keys())
    csv_writer.writeheader()
    for row in joined_rows:
        csv_writer.writerow(row)

        

