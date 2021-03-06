from sklearn.model_selection import RandomizedSearchCV
from cbds.deeplearning import Project, ImageGenerator
from cbds.deeplearning.models.vgg16 import vgg16_like_from_list
from scipy.stats import uniform
from keras.layers import Dense, Dropout, Flatten
from keras.models import Model
from itertools import product
import os


def create_model(input_shape, layer_list):
    base_model = vgg16_like_from_list(input_shape, layer_list)
    x = Flatten()(base_model.output)
    x = Dense(512, activation="relu")(x)
    x = Dropout(0.5)(x)
    predictions = Dense(1, activation="sigmoid")(x)
    model_name = "vgg16_{}_fc512_fc1".format("_".join(["{}_{}".format(layer_type, layer_size)
                                                       for layer_type, layer_size in layer_list]))
    return model_name, Model(base_model.input, predictions)


def create_models(input_shape):
    layer_depths = [64, 128, 256, 512, 512]
    layer_types = ["conv2", "conv3"]
    layer_combinations = [layer_combination for i in range(3, 6) for layer_combination in product(layer_types, repeat=i)]
    return (create_model(input_shape, [(layer_type, layer_depth)
            for layer_type, layer_depth in zip(layer_combination, layer_depths)])
            for layer_combination in layer_combinations
            )


def main():
    project_path = r"/media/megatron/Projects/DeepSolaris"
    project_path = r"/media/tim/Data/Work/CBS/DeepSolaris"
    with Project(project_path=project_path) as project:
        dataset = project.dataset("Heerlen-HR")
        #dataset.import_numpy_dataset(os.path.join(project_path, r"Images/hr_2018_18m_all.npy"),
        #                             os.path.join(project_path, r"Images/hr_2018_18m_all_labels.npy"))

        train_dataset, test_dataset = dataset.split(test_size=0.2)

        image_shape = dataset.data[0].shape
        for name, cnn_model in create_models(input_shape=image_shape):
            model = project.model(name)
            model.create_model(cnn_model)
            cnn_model.summary()
            model.random_search(train_dataset, test_dataset, param_distributions=dict(
                epochs=[3],
                batch_size=[32],
                loss_function=["binary_crossentropy"],
                lr=uniform(0, 0.1),
                momentum=[0.7, 0.8, 0.9],
                nesterov=[True, False],
                decay=[0]
            ))


if __name__ == "__main__":
    main()
