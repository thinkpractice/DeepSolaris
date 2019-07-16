from cbds.deeplearning.models.vgg16 import vgg16_like_from_list
from keras.layers import Flatten, Dropout, Dense
from keras.models import Model


def create_model(input_shape, layer_list):
    base_model = vgg16_like_from_list(input_shape, layer_list)
    x = Flatten()(base_model.output)
    x = Dense(512, activation="relu")(x)
    x = Dropout(0.5)(x)
    predictions = Dense(1, activation="sigmoid")(x)
    model_name = "vgg16_{}_fc512_fc1".format("_".join(["{}_{}".format(layer_type, layer_size)
                                                       for layer_type, layer_size in layer_list]))
    return model_name, Model(base_model.input, predictions)

layer_sizes = [64, 128, 256, 512, 512]
network_structures = [[("conv2", layer_size) for layer_size in layer_sizes[:network_size]] for network_size in range(1, 6)]

for network_structure in network_structures:
    print("Network structure: {}".format(network_structure))
    _, model = create_model(input_shape=(187, 187, 3), layer_list=network_structure)
    model.summary()


