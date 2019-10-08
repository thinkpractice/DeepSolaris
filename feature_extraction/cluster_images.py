from keras.models import load_model, Model
from sklearn.cluster import KMeans, DBSCAN
from hdf5datasetwriter import HDF5DatasetWriter
import keras.applications.vgg16 as vgg16
import argparse
import pickle
import h5py
import os
import numpy as np
import progressbar

def preprocess_images(images):
    return vgg16.preprocess_input(images[:, :, :, ::-1])

def get_features_for_class(db, data_key, label_key):
    i = int(db[label_key].shape[0] * 0.75)
    return db[data_key][:i], db[label_key][:i], db[data_key][i:], db[label_key][i:]

def write_features(model, batch_size, images, labels, feature_vector_size, output_filename):
    dataset = HDF5DatasetWriter((len(images), feature_vector_size), output_filename, dataKey="features",
                                bufSize=1000)
    widgets = ["Extracting Features: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
    pbar = progressbar.ProgressBar(maxval=len(images), widgets=widgets).start()
    for i in np.arange(0, len(images), batch_size):
        images_for_batch = images[i:i + batch_size, :]
        batchLabels = labels[i:i + batch_size]

        features = model.predict(images_for_batch, batch_size=batch_size)
        features = features.reshape((features.shape[0], feature_vector_size))
        dataset.add(features, batchLabels)
        pbar.update(i)
    dataset.close()
    pbar.finish()

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image-file", required=True, help="The numpy file containing the images")
parser.add_argument("-l", "--labels", required=True, help="path to input labels")
parser.add_argument("-m", "--model", required=True, help="path to the model used to extract features")
parser.add_argument("-n", "--layer-name", default="block5_pool", help="The name of the layer to use for feature extraction")
parser.add_argument("-b", "--batch-size", type=int, default=32, help="batch size of images to be passed through network")
parser.add_argument("-d", "--db", required=True, help="path HDF5 database")
parser.add_argument("-s", "--distance-metric", default="cosine", help="The pairwise distance metric to use")
parser.add_argument("-o", "--output", required=True, help="The output directory to store the clusters")
args = vars(parser.parse_args())

model = load_model(args["model"])
last_layer = model.get_layer(name=args["layer_name"])

print("Loading the images")
orig_images = np.load(args["image_file"])
images = preprocess_images(orig_images)
labels = np.load(args["labels"])

feature_vector_size = np.prod(last_layer.output_shape[1:])
print("Feature vector size: {}".format(feature_vector_size))
feature_model = Model(inputs=model.layers[0].input, outputs=last_layer.output)

if not os.path.exists(args["db"]):
    print("Extracting features from {}".format(args["image_file"]))
    write_features(feature_model, args["batch_size"], images, labels, feature_vector_size, args["db"])

print("Clustering...")
db = h5py.File(args["db"], "r")
#clustering_algorithm = DBSCAN(metric=args["distance_metric"])
clustering_algorithm = KMeans()
clustering_algorithm.fit(db["features"])
print("Found {} clusters".format(len(np.unique(clustering_algorithm.labels_))))

print("Writing image clusters to disk...")
for label in np.unique(clustering_algorithm.labels_):
    cluster_images = orig_images[np.where(clustering_algorithm.labels_ == label),:]
    print("Cluster images shape: {}".format(cluster_images.shape))
    np.save(os.path.join(args["output"], "{}.npy".format(label)), cluster_images)

