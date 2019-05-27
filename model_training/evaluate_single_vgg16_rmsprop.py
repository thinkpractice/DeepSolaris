from sklearn.model_selection import RandomizedSearchCV
from cbds.deeplearning import Project, ImageGenerator
from cbds.deeplearning import ImageGenerator
from cbds.deeplearning.settings import RMSPropSettings
from cbds.deeplearning.models.vgg16 import vgg16
from cbds.deeplearning.metrics import ClassificationReportCallback, ConfusionMatrixCallback, PlotRocCallback
from scipy.stats import uniform
from keras.layers import Dense, Dropout, Flatten
from keras.models import Model
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from itertools import product
import os


def create_vgg16_model(input_shape, layer_index=15):
    base_model = vgg16(input_shape, include_top=False, batch_normalization=False)
    for layer in base_model.layers[:layer_index]:
        layer.trainable = False
    for layer in base_model.layers[layer_index:]:
        layer.trainable = False
    x = Flatten()(base_model.output)
    #x = Dense(512, activation="relu")(x)
    #x = Dropout(0.5)(x)
    predictions = Dense(1, activation="sigmoid")(x)
    model_name = "vgg16_full_fc512_fc1_aug_frozen_rms_prop"
    return model_name, Model(base_model.input, predictions)


def main():
    #project_path = r"/media/megatron/Projects/DeepSolaris"
    project_path = r"/media/tim/Data/Work/CBS/DeepSolaris"
    with Project(project_path=project_path) as project:
        dataset = project.dataset("Heerlen-HR")
        dataset.data = dataset.data[:,:,:,::-1]

        train_dataset, test_dataset = dataset.split(test_size=0.2)

        train_generator = ImageGenerator(train_dataset)\
                          .with_rescale(1/255.)\
                          .with_seed(42)\
                          .with_rotation_range(30)\
                          .with_width_shift_range(0.1)\
                          .with_height_shift_range(0.1)\
                          .with_zoom_range(0.2)\
                          .with_shear_range(0.2)\
                          .with_horizontal_flip(True)\
                          .with_fill_mode("reflect")

        test_generator = ImageGenerator(test_dataset)\
                         .with_rescale(1/255.)\
                         .with_seed(84)

        image_shape = dataset.data[0].shape

        name, cnn_model = create_vgg16_model(input_shape=image_shape, layer_index=7)

        model = project.model(name)
        model.create_model(cnn_model)
        model.plot()
        cnn_model.summary()

        #        .with_callbacks([EarlyStopping(patience=5)])\
        with model.run().with_epochs(10)\
                .with_batch_size(32)\
                .with_loss_function("binary_crossentropy")\
                .with_optimizer(RMSPropSettings())\
                .with_metric_callbacks([ClassificationReportCallback(), ConfusionMatrixCallback(), PlotRocCallback()])\
                .with_class_weights(train_dataset.class_weights)\
                .with_train_dataset(train_generator)\
                .with_test_dataset(test_generator)\
                .with_evaluation_dataset(test_dataset) as run:
                run.train()
                run.evaluate()


if __name__ == "__main__":
    main()
