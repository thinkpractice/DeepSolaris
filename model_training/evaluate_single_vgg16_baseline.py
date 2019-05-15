from sklearn.model_selection import RandomizedSearchCV
from cbds.deeplearning import Project, ImageGenerator
from cbds.deeplearning.models.vgg16 import vgg16
from scipy.stats import uniform
from keras.layers import Dense, Dropout, Flatten
from keras.models import Model
from keras.callbacks import EarlyStopping
from itertools import product
import os


def create_vgg16_model(input_shape):
    base_model = vgg16(input_shape, include_top=False, batch_normalization=False)
    x = Flatten()(base_model.output)
    x = Dense(512, activation="relu")(x)
    predictions = Dense(1, activation="sigmoid")(x)
    model_name = "vgg16_full_fc512_fc1_baseline"
    return model_name, Model(base_model.input, predictions)

def main():
    project_path = r"/media/megatron/Projects/DeepSolaris"
    #project_path = r"/media/tim/Data/Work/CBS/DeepSolaris"
    with Project(project_path=project_path) as project:
        dataset = project.dataset("Heerlen-HR")

        train_dataset, test_dataset = dataset.split(test_size=0.2)

        image_shape = dataset.data[0].shape
        
        name, cnn_model = create_vgg16_model(input_shape=image_shape)

        model = project.model(name)
        model.create_model(cnn_model)
        model.plot()
        cnn_model.summary()

        model.random_search(train_dataset, test_dataset, param_distributions=dict(
            epochs=[40],
            batch_size=[32],
            loss_function=["binary_crossentropy"],
            lr=uniform(1e-1, 1e-6),
            momentum=[0.7, 0.8, 0.9],
            nesterov=[True, False],
            decay=[0],
            callbacks=[[EarlyStopping(patience=5)]],
        ), n_iter=15)


if __name__ == "__main__":
    main()

