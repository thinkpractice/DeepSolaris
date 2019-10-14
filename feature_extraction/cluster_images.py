from keras.models import load_model, Model
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.neighbors import NearestNeighbors
from hdf5datasetwriter import HDF5DatasetWriter
import matplotlib.pyplot as plt
import keras.applications.vgg16 as vgg16
import argparse
import pickle
import h5py
import os
import numpy as np
import progressbar
import cv2

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image-file", required=True, help="The numpy file containing the images")
parser.add_argument("-l", "--labels", required=True, help="path to input labels")
parser.add_argument("-d", "--db", required=True, help="path HDF5 database")
parser.add_argument("-s", "--distance-metric", default="cosine", help="The pairwise distance metric to use")
parser.add_argument("-e", "--eps", default=0.5, type=float, help="The eps value for dbscan")
parser.add_argument("-o", "--output", required=True, help="The output directory to store the clusters")
parser.add_argument("-k", "--knn-range", default=1000, type=int, help="The range of k to explore for the knn")
args = vars(parser.parse_args())

print("Loading the images")
orig_images = np.load(args["image_file"])
labels = np.load(args["labels"])

print("Loading features")
db = h5py.File(args["db"], "r")
features = db["features"]
D = pairwise_distances(features, metric=args["distance_metric"])
D = np.where(D==0, D.mean(), D)
plt.hist(D.flatten(), bins=100)
plt.show()
print("Min distance: {}, Max distance: {}, Avg distance: {}".format(D.min(), D.max(), D.mean()))

print("Nearest neighbours calculation")
widgets = ["KNN: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(maxval=args["knn_range"], widgets=widgets).start()
k_distances = dict()
for k in range(1, args["knn_range"]):
    knn = NearestNeighbors(n_neighbors=k, metric=args["distance_metric"], n_jobs=-1)
    knn.fit(features)
    dist, _ = knn.kneighbors(features)
    k_distances[k] = dist.mean()
    pbar.update(k)
pbar.finish()

plt.scatter(k_distances.keys(), k_distances.values())
plt.show()

print("Clustering...")
#clustering_algorithm = DBSCAN(metric=args["distance_metric"], eps=args["eps"])
clustering_algorithm = KMeans(n_clusters=4)
clustering_algorithm.fit(features)
print("Found {} clusters".format(len(np.unique(clustering_algorithm.labels_))))

print("Writing image clusters to disk...")
for label in np.unique(clustering_algorithm.labels_):
    cluster_images = orig_images[np.where(clustering_algorithm.labels_ == label)[0],:]
    print("Cluster images shape: {}".format(cluster_images.shape))
    output_path = os.path.join(args["output"], "{}".format(label))
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for index, image in enumerate(cluster_images):
        filename = os.path.join(output_path, "{}.png".format(index))
        cv2.imwrite(filename, image)

