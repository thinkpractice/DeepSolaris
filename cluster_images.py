import argparse
import numpy as np
from keras.models import load_model
from sklearn.cluster import DBSCAN
import os

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="The input dataset with images to cluster")
parser.add_argument("-m", "--model", required=True, help="The CNN model to use for clustering")
parser.add_argument("-l", "--layer", required=True, help="The layer which output is used for clustering")
parser.add_argument("-d", "--distance-metric", default="cosine_similarity", help="The pairwise distance metric to use")
parser.add_argument("-o", "--output", required=True, help="The output directory to store the clusters")
args = vars(parser.parse_args())

print("Loading images from {}".format(args["input"]))
images = np.load(args["input"]) 

print("Extracting features...")
model = load_model(args["model"])
model.summary()
features = model.predict(images)

print("Clustering...")
dbscan = DBSCAN(metric=args["distance_metric"])
dbscan.fit(features)

print("Writing image clusters to disk...")
for label in np.unique(dbscan.labels_):
    cluster_images = images[np.where(dbscan.labels_ == label),:]
    np.save(os.path.join(args["output"], "{}.npy".format(label)), cluster_images)

