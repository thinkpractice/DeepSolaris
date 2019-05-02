from sklearn.model_selection import RandomizedSearchCV
from cbds.deeplearning import Project, ImageGenerator
from cbds.deeplearning.models.vgg16 import vgg16_like_from_list
from scipy.stats import randint as sp_randint 
from scipy.stats import uniform
from keras.layers import Dense, Dropout, Flatten

def create_model(input_shape, layer_list):
    vgg16_conv = vgg16_like_from_list(input_shape, layer_list)
    x = Flatten()(vgg16_conv.output)
    x = Dense(512, activation="relu")(x)
    x = Dropout(0.5)(x)
    predictions = Dense(1, activation="sigmoid")(x)
    return Model(base_model.input, predictions)

def create_models(input_shape):
    layer_depths = [64, 128, 256, 512, 512]
    layer_types = ["conv2", "conv3"]
    layer_combinations = [layer_combination for i in range(6) for layer_combination in product(layer_types, repeat=i)]
    return [create_model(input_shape, [(layer_type, layer_depth)
            for layer_type, layer_depth in zip(layer_combination, layer_depths)])
            for layer_combination in layer_combinations
            ]

def main():
    with Project(project_path=r"/media/megatron/Projects/DeepSolaris") as project:
        dataset = project.dataset("Heerlen-HR")
        #dataset.import_numpy_dataset(r"/media/megatron/9827-B092/hr_2018_18m_all.npy", r"/media/megatron/9827-B092/hr_2018_18m_all_labels.npy")


        train_dataset, test_dataset = dataset.split(test_size=0.2)
        train_generator = ImageGenerator(train_dataset)\
                            .with_shuffle_data(True)\
                            # .with_rotation_range(45)\
                            # .with_width_shift_range(0.1)\
                            # .with_height_shift_range(0.1)\
                            # .with_shear_range(0.1)\
                            # .with_zoom_range(0.1)\
                            # .with_channel_shift_range(0.1)\
                            # .with_horizontal_flip(0.1)\
                            .with_rescale(1./255)
        test_generator = ImageGenerator(test_dataset)\
                            .with_rescale(1./255)

        print("Number of training items: {}".format(len(train_dataset)))
        print("Number of testing items: {}".format(len(test_dataset)))

        image_shape = train_dataset.data[0].shape
        for name, cnn_model in create_models(input_shape=image_shape):
            model = project.model(name)
            model.create_model(cnn_model)
            keras_model = model.get_keras_classifier_model(epochs=100, batch_size=32, loss_function="binary_crossentropy", train_dataset=train_dataset, test_dataset=test_dataset)

            randomized_search = RandomizedSearchCV(keras_model, param_distributions={
                    "learn_rate": uniform(),
                    "momentum": [0.7, 0.8, 0.9],
                    "nesterov": [True, False]
                })


if __name__ == "__main__":
    main()
