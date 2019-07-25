from skimage import exposure
from skimage import feature
import cv2
import argparse
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", required=True,
                        help="The image to show the histogram of oriented gradients for")
    parser.add_argument("-o", "--output", help="The output file to write the image to")
    args = vars(parser.parse_args())

    image = cv2.imread(args["image"])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    (H, hog_image) = feature.hog(gray, orientations=9, pixels_per_cell=(8, 8),
                                 cells_per_block=(2, 2), transform_sqrt=True, block_norm="L1",
                                 visualize=True)
    hog_image = exposure.rescale_intensity(hog_image, out_range=(0, 255))
    hog_image = hog_image.astype("uint8")

    cv2.imshow("Images", image)
    cv2.imshow("HOG", hog_image)
    cv2.waitKey(0)

    output_filename = args.get("output", None)
    if output_filename:
        cv2.imwrite(output_filename, hog_image)


if __name__ == "__main__":
    main()
