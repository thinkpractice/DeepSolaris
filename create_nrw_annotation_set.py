import csv
import argparse
from pyproj import Proj, transform

def convert_coordinate(in_proj, out_proj, x, y):
    inProj = Proj(init=in_proj)
    outProj = Proj(init=out_proj)
    return transform(inProj, outProj, x, y)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="The input file containing all annotations")
parser.add_argument("-o", "--output", required=True, help="The output file with a column selection and possibly reprojected")
parser.add_argument("-p", "--projection", default="25832", help="The output projection, should be a projection in meters (default: epsg:25832)")
args = vars(parser.parse_args())

mapped_rows = []
with open(args["input"], "r") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=";")
    for row in csv_reader:
        longitude = float(row["lon"].replace(",", "."))
        latitude = float(row["lat"].replace(",", "."))
        projected_x, projected_y =  convert_coordinate("epsg:4326", "epsg:{}".format(args["projection"]), longitude, latitude)

        mapped_rows.append({
                        "object_id": row["OBJECTID"],
                        "lon": longitude,
                        "lat": latitude,
                        "evaluation": row["evaluation"],
                        "label": True if row["evaluation"].lower() == "pos" else False,

                        "x": projected_x,
                        "y": projected_y
                        })


with open(args["output"], "w") as output_file:
    csv_writer = csv.DictWriter(output_file, delimiter=";", fieldnames=["object_id", "lon", "lat", "x", "y", "evaluation", "label"])
    csv_writer.writeheader()
    for row in mapped_rows:
        csv_writer.writerow(row)

