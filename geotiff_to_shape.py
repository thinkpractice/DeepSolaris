from imutils.paths import list_images
from pyproj import Proj, transform
import argparse
import shapefile
import gdal
import os
import progressbar

def get_projection_coords(geo_transform, x, y):
        """This method converts the pixel coordinate (x, y) into the coordinate system used
        by the projection of the map.
        The equations used are:
        Xp = geo_transform[0] + x * geo_transform[1] + y * tranform[2]
        
        Yp = geo_transform[3] + x * geo_transform[4] + y * geo_transform[5]
        
        :param int x: the pixel x coordinate
        
        :param int y: the pixel y coordinate
        :return: a tuple with the coordinates in projection space.
        :rtype: tuple (double, double)
        """
        Xp = geo_transform[0] + x * geo_transform[1] + y * geo_transform[2]
        Yp = geo_transform[3] + x * geo_transform[4] + y * geo_transform[5]
        return (Xp, Yp)


def to_rd(coordinate):
    gpsProjection = Proj(init='epsg:4326')
    mapProjection = Proj(init='epsg:28992')
    return transform(gpsProjection, mapProjection, coordinate[0], coordinate[1])


def get_bounding_box(geo_transform, width, height):
    top_left = get_projection_coords(geo_transform, 0, 0)
    bottom_right = get_projection_coords(geo_transform, width, height)
    return [to_rd(top_left), to_rd(bottom_right)]


def get_polygon(bounding_box):
    return[
            [
                [bounding_box[0][0], bounding_box[0][1]],
                [bounding_box[1][0], bounding_box[0][1]],
                [bounding_box[1][0], bounding_box[1][1]],
                [bounding_box[0][0], bounding_box[1][1]],
                [bounding_box[0][0], bounding_box[0][1]],
            ]
        ]


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset", required=True, help="The folder for the dataset to extract the geoinformation from")
parser.add_argument("-o", "--output", required=True, help="The output shapefile for the geoinformation")
args = vars(parser.parse_args())

with shapefile.Writer(args["output"]) as shp:
    shp.field('FILENAME', 'C')
    shp.field('UUID', 'C', size=37)

    widgets = ["Classifying images: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]

    image_paths = [image_path for image_path in list_images(args["dataset"]) if "mask" not in image_path and image_path.endswith(".tiff")]
    pbar = progressbar.ProgressBar(maxval=len(image_paths), widgets=widgets).start()
    for i, image_path in enumerate(image_paths):
        dataset = gdal.Open(image_path) 
        geo_transform = dataset.GetGeoTransform()
        bounding_box = get_bounding_box(geo_transform, dataset.RasterXSize, dataset.RasterYSize)
        uuid = os.path.basename(image_path)[:37]
        shp.record(image_path, uuid) 
        shp.poly(get_polygon(bounding_box))
        pbar.update(i)
    pbar.finish()

