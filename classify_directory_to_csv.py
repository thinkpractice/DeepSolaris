from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing.image import load_img, save_img, img_to_array
import progressbar
import argparse
import os
import csv
import numpy as np


def load_image(filename):
    image = load_img(filename, target_size=(187, 187))
    image = img_to_array(image)
    image = image[:,:,::-1]
    return preprocess_input(image)

def predictions_for(predictions, one_hot=False): 
    if one_hot:
        return np.argmax(predictions, axis=1)
    return predictions

def get_class(prediction, one_hot):
    if one_hot:
        return prediction
    return 1 if prediction >= args["cut_off"] else 0

def get_uuid(filename):
    return os.path.basename(filename)[:36]


ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True, help="Model to use for classification")
ap.add_argument("-d", "--dataset", required=True, help="The dataset to classify")
ap.add_argument("-o", "--output", required=True, help="The output csv with the uuid, prediction, and classification")
ap.add_argument("-b", "--batch-size", type=int, default=32, help="The batchsize to use when classifying the images")
ap.add_argument("-c", "--cut-off", type=float, default=0.5, help="The cut-off to use when classifying the images")
args = vars(ap.parse_args())

model = load_model(args["model"])
one_hot = model.get_layer(index=-1).output_shape[-1] > 1

images = [os.path.join(args["dataset"], image) for image in os.listdir(args["dataset"]) if image.endswith(".tiff")]
print("[INFO] processing images")

widgets = ["Classifying images: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(maxval=len(images), widgets=widgets).start()
with open(args["output"], "w") as csv_file:
    csv_writer = DictWriter(csv_file, fieldnames=["uuid", "prediction", "label"], delimiter=";")
    csv_writer.writeheader()
    for i in range(0, len(images), args["batch_size"]):
        image_filenames = images[i:i + args["batch_size"]]
        image_batch = np.stack([load_image(filename) for filename in image_filenames])
        predictions = predictions_for(model.predict(image_batch, batch_size=args["batch_size"]), one_hot)
        for filename, prediction, image in zip(image_filenames, predictions, image_batch):
            csv_writer.writerow({"uuid": get_uuid(filename), "prediction": prediction, "label": get_class(prediction, one_hot)})
        pbar.update(i)
print("[INFO] finished processing")
pbar.finish()

