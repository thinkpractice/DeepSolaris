from keras.models import load_model
from keras.utils import to_categorical
from keras.applications.vgg16 import preprocess_input
from sklearn.metrics import classification_report, confusion_matrix
import argparse
import numpy as np
import os


def get_paths(path):
    return (os.path.join(path, filename) for filename in os.listdir(path) if os.path.isfile(os.path.join(path, filename)))


def get_numpy_datasets(path):
    return [filename for filename in get_paths(path) if filename.endswith(".npy") and not filename.endswith("labels.npy")]


def get_numpy_labels(filename, one_hot=False):
    dataset_name, _ = os.path.splitext(filename)
    label_filename = "{}_labels.npy".format(dataset_name)
    labels = np.load(label_filename)
    return to_categorical(labels) if one_hot else labels

def evaluate(labels, predictions, one_hot=False):
    if one_hot:
        predictions = np.argmax(predictions, axis=1)       
        labels = np.argmax(labels, axis=1)
    print(classification_report(labels, predictions))
    print(confusion_matrix(labels, predictions))


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input-directory", required=True, help="The input directory containing the numpy datasets")
parser.add_argument("-m", "--model", required=True, help="The trained keras model to evaluate the numpy datasets")
args = vars(parser.parse_args())

model = load_model(args["model"])
one_hot = model.get_layer(index=-1).output_shape[-1] > 1
for dataset_filename in get_numpy_datasets(args["input_directory"]):
    labels = get_numpy_labels(dataset_filename, one_hot)    
    images = np.load(dataset_filename)
    images = preprocess_input(images[:,:,:,::-1])
    predictions = np.round(model.predict(images)) 
    evaluate(labels, predictions, one_hot)

