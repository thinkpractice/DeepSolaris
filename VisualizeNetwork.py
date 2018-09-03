'''Visualization of the filters of VGG16, via gradient ascent in input space.
This script can run on CPU in a few minutes.
Results example: http://i.imgur.com/4nj4KjN.jpg
'''
import numpy as np
import time
import sys
import argparse
from keras.preprocessing.image import save_img
from keras import backend as K
from ModelFactory import ModelFactory

def deprocess_image(x):
    # normalize tensor: center on 0., ensure std is 0.1
    x -= x.mean()
    x /= (x.std() + K.epsilon())
    x *= 0.1

    # clip to [0, 1]
    x += 0.5
    x = np.clip(x, 0, 1)

    # convert to RGB array
    x *= 255
    if K.image_data_format() == 'channels_first':
        x = x.transpose((1, 2, 0))
    x = np.clip(x, 0, 255).astype('uint8')
    return x


def normalize(x):
    # utility function to normalize a tensor by its L2 norm
    return x / (K.sqrt(K.mean(K.square(x))) + K.epsilon())


def visualize_filters(model, layer_name, filter_depth, img_height, img_width):
    # this is the placeholder for the input images
    input_img = model.input
    # get the symbolic outputs of each "key" layer (we gave them unique names).
    layer_dict = dict([(layer.name, layer) for layer in model.layers[1:]])
    kept_filters = []
    for filter_index in range(filter_depth):
        # we only scan through the first 200 filters,
        # but there are actually 512 of them
        print('Processing filter %d' % filter_index)
        start_time = time.time()

        # we build a loss function that maximizes the activation
        # of the nth filter of the layer considered
        layer_output = layer_dict[layer_name].output
        if K.image_data_format() == 'channels_first':
            loss = K.mean(layer_output[:, filter_index, :, :])
        else:
            loss = K.mean(layer_output[:, :, :, filter_index])

        # we compute the gradient of the input picture wrt this loss
        grads = K.gradients(loss, input_img)[0]

        # normalization trick: we normalize the gradient
        grads = normalize(grads)

        # this function returns the loss and grads given the input picture
        iterate = K.function([input_img], [loss, grads])

        # step size for gradient ascent
        step = 1.

        # we start from a gray image with some random noise
        if K.image_data_format() == 'channels_first':
            input_img_data = np.random.random((1, 3, img_width, img_height))
        else:
            input_img_data = np.random.random((1, img_width, img_height, 3))
        input_img_data = (input_img_data - 0.5) * 20 + 128

        # we run gradient ascent for 20 steps
        loss_value = 0
        for i in range(20):
            loss_value, grads_value = iterate([input_img_data])
            input_img_data += grads_value * step

            print('Current loss value:', loss_value)
            if loss_value <= 0.:
                # some filters get stuck to 0, we can skip them
                break

        # decode the resulting input image
        img = deprocess_image(input_img_data[0])
        kept_filters.append((img, loss_value))
        end_time = time.time()
        print('Filter %d processed in %ds' % (filter_index, end_time - start_time))
    return kept_filters


def create_filter_visualization(img_height, img_width, kept_filters, number_of_filters, layer_name):
    # the filters that have the highest loss are assumed to be better-looking.
    filter_width = 16
    filter_height = number_of_filters // 16
    print("filter_width={}, filter_height={}, number_of_filters={}".format(filter_width, filter_height, number_of_filters))

    kept_filters.sort(key=lambda x: x[1], reverse=True)
    # build a black picture with enough space for
    margin = 5
    width = filter_width * img_width + (filter_width - 1) * margin
    height = filter_height * img_height + (filter_height - 1) * margin
    print("width={}, height={}".format(width, height))
    stitched_filters = np.zeros((height, width, 3))
    # fill the picture with our saved filters
    for column in range(filter_width):
        for row in range(filter_height):
            img, loss = kept_filters[row * filter_width + column]
            stitched_filters[(img_height + margin) * row: (img_height + margin) * row + img_height,
            (img_width + margin) * column: (img_width + margin) * column + img_width, :] = img

    # save the result to disk
    save_img(layer_name + '_stitched_filters_%dx%d.png' % (filter_height, filter_width), stitched_filters)


def visualize_layer(layer_name, model, height=128, width=128):
    layer = model.get_layer(layer_name)
    kept_filters = visualize_filters(model, layer_name, layer.output_shape[3], height, width)
    create_filter_visualization(height, width, kept_filters, layer.output_shape[3], layer_name)

def visualize_all_layers(model, height=128, width=128):
    for layer in model.layers:
        # we will stitch the best filters on a number_of_filters x number_of_filters grid.
        visualize_layer(layer.name, model, height, width)


def main(argv):
    parser = argparse.ArgumentParser(description='Visualizes Keras neural network models')
    parser.add_argument("model_name", type=str, help="The name of the base model, i.e vgg16, vgg19, etc.")
    parser.add_argument("filename", type=str, help="The model filename")
    parser.add_argument("--width", type=int, help="The width of the generated pictures for each filter", default=128)
    parser.add_argument("--height", type=int, help="The height of the generated pictures for each filter", default=128)
    parser.add_argument("--layer_name", type=str, help="A specific layer to depict", default="")

    args = parser.parse_args()
    model = ModelFactory.load_model_from_file(args.model_name, args.filename)
    if not args.layer_name:
        visualize_all_layers(model, args.height, args.width)
    else:
        visualize_layer(args.layer_name, model, args.height, args.width)


if __name__ == "__main__":
    main(sys.argv)
