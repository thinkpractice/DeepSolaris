from keras.applications import VGG16
from keras.applications import imagenet_utils
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from hdf5datasetwriter import HDF5DatasetWriter
from imutils import paths
import numpy as np
import progressbar
import argparse
import random
import os

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="path to input dataset")
ap.add_argument("-l", "--labels", required=True, help="path to input labels")
ap.add_argument("-o", "--output", required=True, help="path to output HDF5 file")
ap.add_argument("-b", "--batch-size", type=int, default=32, help="batch size of images to be passed through network")
ap.add_argument("-s", "--buffer-size",type=int, default=1000, help="size of feature extraction buffer")
args = vars(ap.parse_args())

bs = args["batch_size"]
print("[INFO] loading images...")

images = np.load(args["dataset"])
labels = np.load(args["labels"])

idxs = np.arange(0, images.shape[0])
np.random.shuffle(idxs)

images = images[idxs]
labels = labels[idxs]

print("[INFO] loading network...")
model = VGG16(weights="imagenet", include_top=False)

feature_vector_size = 512 * 5 * 5
dataset = HDF5DatasetWriter((len(images), feature_vector_size), args["output"], dataKey="features", bufSize=args["buffer_size"])
dataset.storeClassLabels(np.unique(labels))

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

