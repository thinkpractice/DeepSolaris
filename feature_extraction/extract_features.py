import argparse

import numpy as np
import progressbar
from hdf5datasetwriter import HDF5DatasetWriter
from keras.applications import imagenet_utils
import keras.applications.vgg16 as vgg16
import keras.applications.xception as xception
from keras.models import load_model


def write_features(model, images, labels, feature_vector_size, data_key, args, class_labels):
    dataset = HDF5DatasetWriter((len(images), feature_vector_size), args["output"], dataKey=data_key,
                                bufSize=args["buffer_size"])
    dataset.storeClassLabels(class_labels)
    widgets = ["Extracting Features: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
    pbar = progressbar.ProgressBar(maxval=len(images), widgets=widgets).start()
    for i in np.arange(0, len(images), bs):
        images_for_batch = images[i:i + bs, :]
        batchLabels = labels[i:i + bs]

        features = model.predict(images_for_batch, batch_size=bs)
        features = features.reshape((features.shape[0], feature_vector_size))
        dataset.add(features, batchLabels)
        pbar.update(i)
    dataset.close()
    pbar.finish()


def randomize_images(images, labels):
    idxs = np.arange(0, images.shape[0])
    np.random.shuffle(idxs)
    images = images[idxs]
    labels = labels[idxs]
    return images, labels


def images_for_class(images, labels, class_label):
    idxs = np.where(labels == class_label)
    selected_images = images[idxs]
    selected_labels = labels[idxs]
    return selected_images, selected_labels


def preprocess_images(images, network_type):
    if network_type.lower() == "vgg16":
        return vgg16.preprocess_input(images[:, :, :, ::-1])
    elif network_type.lower() == "xception":
        return xception.preprocess_input(images[:, :, :, ::-1])
    return imagenet_utils.preprocess_input(images[:, :, :, ::-1])


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="path to input dataset")
ap.add_argument("-l", "--labels", required=True, help="path to input labels")
ap.add_argument("-m", "--model", required=True, help="path to the model used to extract features")
ap.add_argument("-t", "--network-type", default="vgg16", help="The type of network to create")
ap.add_argument("-o", "--output", required=True, help="path to output HDF5 file")
ap.add_argument("-b", "--batch-size", type=int, default=32, help="batch size of images to be passed through network")
ap.add_argument("-s", "--buffer-size",type=int, default=1000, help="size of feature extraction buffer")
args = vars(ap.parse_args())

bs = args["batch_size"]
print("[INFO] loading images...")

images = np.load(args["dataset"])
images = preprocess_images(images, args["network_type"])
labels = np.load(args["labels"])
class_labels = np.unique(labels)
positive_images, positive_labels = images_for_class(images, labels, 1)
positive_images, positive_labels = randomize_images(positive_images, positive_labels)

negative_images, negative_labels = images_for_class(images, labels, 0)
negative_images, negative_labels = randomize_images(negative_images, negative_labels)

print("Split dataset in {} positive images and {} negative".format(positive_labels.shape[0], negative_labels.shape[0]))

print("[INFO] loading network...")
model = load_model(args["model"])
model.summary()

last_layer = model.get_layer(index=-1)
write_features(model, positive_images, positive_labels, last_layer.size, "positive_features", args, class_labels)
write_features(model, negative_images, negative_labels, last_layer.size, "negative_features", args, class_labels)
