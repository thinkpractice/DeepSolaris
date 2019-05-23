from keras.preprocessing.image import ImageDataGenerator
import argparse
import numpy as np
import os

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="The dataset with the images to augment")
ap.add_argument("-o", "--output", required=True, help="The output folder for the augmented images")
ap.add_argument("-n", "--number-of-batches", type=int, default=1, help="The number of batches of images to generate (batch_size=32)")
ap.add_argument("--featurewise-center", default=False, help="Perform featurewise centering or not")
ap.add_argument("--samplewise-center", default=False, help="Perform samplewise centering or not")
ap.add_argument("--featurewise-std-normalization", default=False, help="Perform featurewise std normalization or not")
ap.add_argument("--samplewise-std-normalization", default=False, help="Perform samplewise std normalization or not")
ap.add_argument("--zca-epsilon", default=1e-6, help="Epsilon for zca whitening")
ap.add_argument("--zca-whitening", default=False, help="Perform zca whitening or not")
ap.add_argument("--rotation-range", default=0, type=int, help="Rotation range in degrees")
ap.add_argument("--width-shift-range", default=0, type=float, help="Width shift range")
ap.add_argument("--height-shift-range", default=0, type=float, help="Height shift range")
ap.add_argument("--brightness-range", default=None, type=tuple, help="Brightness range")
ap.add_argument("--shear-range", default=0, type=float,help="Shear intensity")
ap.add_argument("--zoom-range", default=0, type=float, help="Zoom range")
ap.add_argument("--channel-shift-range", default=0, type=float, help="Channel shift range")
ap.add_argument("-f", "--fill-mode", default="nearest", help="The fill_mode used")
ap.add_argument("--cval", default=0.0, help="Value used for points outside the boundaries when fill_mode = contant")
ap.add_argument("--horizontal-flip", default=False, help="Randomly flips inputs horizontally")
ap.add_argument("--vertical-flip", default=False, help="Randomly flips inputs vertically")
ap.add_argument("--rescale", default=None, type=float, help="Rescaling factor")

args = vars(ap.parse_args())

data = np.load(args["dataset"])

if not os.path.exists(args["output"]):
    os.makedirs(args["output"])

image_generator = ImageDataGenerator(featurewise_center=args["featurewise_center"], samplewise_center=args["samplewise_center"], featurewise_std_normalization=args["featurewise_std_normalization"], samplewise_std_normalization=args["samplewise_std_normalization"], zca_epsilon=args["zca_epsilon"], zca_whitening=args["zca_whitening"], rotation_range=args["rotation_range"], width_shift_range=args["width_shift_range"], height_shift_range=args["height_shift_range"], brightness_range=args["brightness_range"], shear_range=args["shear_range"], zoom_range=args["zoom_range"], channel_shift_range=args["channel_shift_range"], fill_mode=args["fill_mode"], cval=args["cval"], horizontal_flip=args["horizontal_flip"], vertical_flip=args["vertical_flip"], rescale=args["rescale"])
generator = image_generator.flow(data, save_to_dir=args["output"])

for _ in range(args["number_of_batches"]):
    next(generator)

