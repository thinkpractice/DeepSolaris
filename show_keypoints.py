import imutils
import cv2
import argparse
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", required=True, help="The image to show the keypoint for")
    parser.add_argument("-k", "--key-point_detector", default="FAST", help="The keypoint detector to use")
    args = vars(parser.parse_args())

    image = cv2.imread(args["image"])
    orig = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    detector = imutils.features.FeatureDetector_create(args["key_point_detector"])

    kps = detector.detect(gray, None)

    print("# of keypoints: {}".format(len(kps)))

    for kp in kps:
        r = int(0.5 * kp.size)
        (x, y) = np.int0(kp.pt)
        cv2.circle(image, (x, y), r, (0, 255, 255), 2)

    cv2.imshow("Images", np.hstack([orig, image]))
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
