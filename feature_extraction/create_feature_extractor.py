from keras.applications import VGG16, Xception
from keras.models import Model
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-l", "--layer", required=True, help="Name of layer until which the network should be kept")
ap.add_argument("-o", "--output", required=True, help="Path to where the model file should be saved")
ap.add_argument("-t", "--network-type", default="vgg16", help="The type of network to create")
ap.add_argument("-s", "--input-shape", nargs="+", type=int, default=(187, 187, 3), help="Input shape to first layer of network")
args = vars(ap.parse_args())

model = None

if args["network_type"].lower() == "xception":
    model = Xception(input_shape=tuple(args["input_shape"]), weights="imagenet", include_top=False, pooling="avg")
else:
    model = VGG16(input_shape=tuple(args["input_shape"]), weights="imagenet", include_top=False)


last_layer = model.get_layer(name=args["layer"])

extractor_model = Model(model.input, last_layer.output)
extractor_model.save(args["output"])
