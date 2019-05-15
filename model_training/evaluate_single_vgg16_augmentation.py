from sklearn.model_selection import RandomizedSearchCV
from cbds.deeplearning import Project, ImageGenerator
from cbds.deeplearning import ImageGenerator
from cbds.deeplearning.models.vgg16 import vgg16
from scipy.stats import uniform
from keras.layers import Dense, Dropout, Flatten
from keras.models import Model
from keras.callbacks import EarlyStopping
from itertools import product
import os


def create_vgg16_model(input_shape):
    base_model = vgg16(input_shape, include_top=False)
    x = Flatten()(base_model.output)
    x = Dense(512, activation="relu")(x)
    x = Dropout(0.5)(x)
    predictions = Dense(1, activation="sigmoid")(x)
    model_name = "vgg16_full_fc512_fc1_aug_reduce_lr"
    return model_name, Model(base_model.input, predictions)


def main():
    project_path = r"/media/megatron/Projects/DeepSolaris"
    # project_path = r"/media/tim/Data/Work/CBS/DeepSolaris"
    with Project(project_path=project_path) as project:
        dataset = project.dataset("Heerlen-HR")

        train_dataset, test_dataset = dataset.split(test_size=0.2)
        train_generator = ImageGenerator(train_dataset)\
                          .with_rescale(1/255.)\
                          .with_seed(42)\
                          .with_rotation_range(30)\
                          .with_width_shift_range(0.1)\
                          .with_width_height_shift_range(0.1)\
                          .with_zoom_range(0.1)\
                          .with_horizontal_flip(True)

        test_generator = ImageGenerator(test_dataset)\
                         .with_rescale(1/255.)\
                         .with_seed(84)

        image_shape = dataset.data[0].shape

        name, cnn_model = create_vgg16_model(input_shape=image_shape)

        model = project.model(name)
        model.create_model(cnn_model)
        model.plot()
        cnn_model.summary()


        model.random_search(train_generator, test_generator, param_distributions=dict(
            epochs=[40],
            batch_size=[32],
            loss_function=["binary_crossentropy"],
            lr=[1e-4],
            momentum=[0.9],
            nesterov=[False],
            calculate_decay=[True],
            callbacks=[[EarlyStopping(patience=5)]],
        ), n_iter=10)


if __name__ == "__main__":
    main()
