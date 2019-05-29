from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing.image import load_img, save_img
import progressbar
import argparse
import os

def load_image(filename):
    image = load_img(filename)
    image = image[:,:,::-1]
    return preprocess_input(image)

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True, help="Model to use for classification")
ap.add_argument("-d", "--dataset", required=True, help="The dataset to classify")
ap.add_argument("-o", "--output", required=True, help="Output dir of classified images")
ap.add_argument("-b", "--batchsize", type=int, default=32, help="The batchsize to use when classifying the images")
ap.add_argument("-c", "--cut-off", type=float, default=0.5, help="The cut-off to use when classifying the images")
args = vars(ap.parse_args())

model = load_model(args["model"])

images = [image for image in os.listdir(args["dataset"]) if image.endswith(".tiff")]
positives_dir = os.path.join(args["output"], "positives")
negatives_dir = os.path.join(args["output"], "negatives")
print("[INFO] processing images")

pbar = progressbar.ProgressBar(maxval=len(images), widgets=widgets).start()
for i in range(0, len(images), args["batch_size"]):
    image_filenames = images[i:i + args["batch_size"])
    image_batch = [load_image(filename) for filename in image_filenames]
    predictions = model.predict(image_batch)
    for filename, prediction in zip(image_filenames, predictions):
        if prediction >= args["cut-off"]:
            save_img(os.path.join(positives_dir, os.path.basename(filename)))
            continue
        save_img(os.path.join(negatives_dir, os.path.basename(filename)))
    pbar.update(i)
print("[INFO] finished processing")        
pbar.finish()

