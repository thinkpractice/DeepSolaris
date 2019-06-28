import cv2
import argparse
import numpy as np
from imutils.feature import FeatureDetector_create


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", required=True, help="The image to show the keypoint for")
    parser.add_argument("-k", "--key-point_detector", default="FAST", help="The keypoint detector to use")
    parser.add_argument("-o", "--output", help="The output file to write the image to")
    args = vars(parser.parse_args())

    image = cv2.imread(args["image"])
    orig = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    detector = FeatureDetector_create(args["key_point_detector"])

    kps = detector.detect(gray)

    print("# of keypoints: {}".format(len(kps)))

    for kp in kps:
        r = int(0.5 * kp.size)
        (x, y) = np.int0(kp.pt)
        cv2.circle(image, (x, y), r, (0, 255, 255), 2)

    combined_image = np.hstack([orig, image])
    cv2.imshow("Images", combined_image)
    cv2.waitKey(0)

    output_filename = args.get("output", None)
    if output_filename:
        cv2.imwrite(output_filename, combined_image)


if __name__ == "__main__":
    main()
