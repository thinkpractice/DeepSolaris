from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing.image import load_img, save_img, img_to_array
import progressbar
import argparse
import os
import numpy as np

def load_image(filename):
    image = load_img(filename, target_size=(187, 187))
    image = img_to_array(image)
    image = image[:,:,::-1]
    return preprocess_input(image)

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True, help="Model to use for classification")
ap.add_argument("-d", "--dataset", required=True, help="The dataset to classify")
ap.add_argument("-o", "--output", required=True, help="Output dir of classified images")
ap.add_argument("-b", "--batch-size", type=int, default=32, help="The batchsize to use when classifying the images")
ap.add_argument("-c", "--cut-off", type=float, default=0.5, help="The cut-off to use when classifying the images")
args = vars(ap.parse_args())

model = load_model(args["model"])

images = [os.path.join(args["dataset"], image) for image in os.listdir(args["dataset"]) if image.endswith(".tiff")]
positives_dir = os.path.join(args["output"], "positives")
if not os.path.exists(positives_dir):
    os.makedirs(positives_dir)
negatives_dir = os.path.join(args["output"], "negatives")
if not os.path.exists(negatives_dir):
    os.makedirs(negatives_dir)
print("[INFO] processing images")

widgets = ["Classifying images: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(maxval=len(images), widgets=widgets).start()
for i in range(0, len(images), args["batch_size"]):
    image_filenames = images[i:i + args["batch_size"]]
    image_batch = np.stack([load_image(filename) for filename in image_filenames])
    predictions = model.predict(image_batch, batch_size=args["batch_size"])
    for filename, prediction, image in zip(image_filenames, predictions, image_batch):
        original = load_img(filename)
        if prediction >= args["cut_off"]:
            save_img(os.path.join(positives_dir, os.path.basename(filename)), original)
            continue
        save_img(os.path.join(negatives_dir, os.path.basename(filename)), original)
    pbar.update(i)
print("[INFO] finished processing")
pbar.finish()

