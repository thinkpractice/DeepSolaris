from sklearn.model_selection import train_test_split
import argparse
import numpy as np
import os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--dataset", required=True, help="The source dataset to split up")
    ap.add_argument("-l", "--labels", required=True, help="The label set to split up")
    ap.add_argument("-p", "--test-percentage", default=0.20, type=float,
                    help="The percentage that should be split as test set")
    ap.add_argument("-v", "--validation-percentage", default=0.50, type=float,
                    help="The percentage that should be split (from the test set) as validation set")
    args = vars(ap.parse_args())

    dataset_filename = args["dataset"]
    labels_path = args["labels"]

    dataset = np.load(dataset_filename)
    labels = np.load(labels_path)

    trainX, validation_testX, trainY, validation_testY = train_test_split(dataset, labels,
                                                                          test_size=args["test_percentage"],
                                                                          stratify=labels)
    testX, validationX, testY, validationY = train_test_split(validation_testX, validation_testY,
                                                              test_size=args["validation_percentage"],
                                                              stratify=validation_testY)

    base_filename = os.path.basename(dataset_filename)
    filename, _ = os.path.splitext(base_filename)
    dataset_path = os.path.dirname(dataset_filename)
    train_filename = os.path.join(dataset_path, "{}_train.npy".format(filename))
    test_filename = os.path.join(dataset_path, "{}_test.npy".format(filename))
    validation_filename = os.path.join(dataset_path, "{}_validation.npy".format(filename))

    print("Writing {}".format(train_filename))
    np.save(train_filename, trainX)
    print("Writing {}".format(test_filename))
    np.save(test_filename, testX)
    print("Writing {}".format(train_filename))
    np.save(validation_filename, validationX)

    labels_base_filename = os.path.basename(labels_path)
    labels_filename, _ = os.path.splitext(labels_base_filename)
    labels_output_path = os.path.dirname(labels_path)
    train_labels_filename = os.path.join(labels_output_path, "{}_train_labels.npy".format(labels_filename))
    test_labels_filename = os.path.join(labels_output_path, "{}_test_labels.npy".format(labels_filename))
    validation_labels_filename = os.path.join(labels_output_path, "{}_validation_labels.npy".format(labels_filename))

    print("Writing {}".format(train_labels_filename))
    np.save(train_labels_filename, trainY)
    print("Writing {}".format(test_labels_filename))
    np.save(test_labels_filename, testY)
    print("Writing {}".format(validation_labels_filename))
    np.save(validation_labels_filename, validationY)


if __name__ == "__main__":
    main()
