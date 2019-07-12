import argparse
import csv
import os
import progressbar
import shapefile
from owslib.wms import WebMapService

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_tile(wms_service, layer_name, longitude, latitude, width_in_pixels, dop_resolution, image_format):
    wms = WebMapService(wms_service, version='1.1.1')
    width_in_meters = width_in_pixels / float(dop_resolution)
    width_from_center = width_in_meters / 2.0
    # This creates a rectangular bounding box for every tile
    bounding_box = (longitude - width_from_center, 
                    latitude - width_from_center,
                    longitude + width_from_center,
                    latitude + width_from_center)

    return wms.getmap(layers=[layer_name], styles=['default'], srs='EPSG:25832',
                bbox=bounding_box, 
                size=(width_in_pixels, width_in_pixels), format=image_format, transparent=True)

def write_image(filename, image):
    with open(filename, 'wb') as image_file:
        image_file.write(image.read())

def get_number_of_images_csv(filename):
    number_of_images = 0
    with open(filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        for row in csv_reader:
            number_of_images += 1

    return number_of_images

def get_number_of_images_shp(filename):
    with shapefile.Reader(filename) as shp:
        return len(shp.shapeRecords())

def get_number_of_images(filename):
    return get_number_of_images_csv(filename) if filename.endswith(".csv") else get_number_of_images_shp(filename)


def get_locations_from_csv(filename, output_directory, image_extension):
    with open(filename, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=";")
        for i, row in enumerate(csv_reader):
            object_id = row["object_id"]
            longitude = float(row["x"])
            latitude = float(row["y"])
            label = "positive" if row["label"].lower() == "true" else "negative"
            
            yield object_id, longitude, latitude, label

def get_locations_from_shapefile(filename, output_directory, image_extension):
    with shapefile.Reader(filename) as shp:
        for i, record in enumerate(shp.shapeRecords()):
            object_id = record.record["LANUV_ID"]
            point = record.shape.points
            label = "positive"

            yield object_id, point[0][0], point[0][1], label 


def get_locations(filename, output_directory, image_format):
    yield from get_locations_from_csv(filename, output_directory, image_format) if filename.endswith(".csv") else get_locations_from_shapefile(filename, output_directory, image_format)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="The input csv file with the coordinates and annotations")
parser.add_argument("-o", "--output", required=True, help="The output directory")
parser.add_argument("-m", "--metadata-file", default="image_metadata.csv", help="The filename that stores the metadata for each file")
parser.add_argument("-s", "--wms_service", default="https://www.wms.nrw.de/geobasis/wms_nw_dop", help="The wms service to download pictures from")
parser.add_argument("-l", "--layer", default="nw_dop_rgb", help="The layer to download from")
parser.add_argument("-w", "--width", default=200, type=int, help="Tile width")
parser.add_argument("-d", "--dop", default=10, type=int, help="The DOP resolution of the image")
parser.add_argument("-f", "--image-format", default="image/png", type=str, help="The image format to download")
args = vars(parser.parse_args())

create_dir(args["output"])
create_dir(os.path.join(args["output"], "positive"))
create_dir(os.path.join(args["output"], "negative"))

number_of_images = get_number_of_images(args["input"])
widgets = ["Downloading images: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(maxval=number_of_images, widgets=widgets).start()

image_extension = args["image_format"].split("/")[-1]
output_directory = args["output"]
metadata_filename = os.path.join(output_directory, args["metadata_file"])
with open(metadata_filename, "w") as metadata_file:
    csv_writer = csv.DictWriter(metadata_file, delimiter=";", fieldnames=["index", "object_id", "longitude", "latitude", "image_filename"])
    csv_writer.writeheader()
    for i, (object_id, longitude, latitude, label) in enumerate(get_locations(args["input"], args["output"], image_extension)):
        tile_image = download_tile(args["wms_service"], args["layer"], longitude, latitude, args["width"], args["dop"], args["image_format"])

        output_path = os.path.join(os.path.join(output_directory, label))
        output_path = os.path.join(output_path, "{}.{}".format(i, image_extension))
    
        write_image(output_path, tile_image)
        csv_writer.writerow({"index": i, "object_id": object_id, "longitude": longitude, "latitude": latitude, "image_filename": output_path})
        pbar.update(i)

pbar.finish()
