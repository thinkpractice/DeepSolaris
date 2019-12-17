from sklearn.model_selection import RandomizedSearchCV
from cbds.deeplearning import Project, ImageGenerator
from cbds.deeplearning import ImageGenerator
from cbds.deeplearning.settings import RMSPropSettings
from cbds.deeplearning.models.vgg16 import vgg16
from cbds.deeplearning.metrics import ClassificationReportCallback, ConfusionMatrixCallback, PlotRocCallback
from scipy.stats import uniform
from keras.layers import Dense, Dropout, Flatten, GlobalAveragePooling2D
from keras.models import Model
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.applications.vgg16 import preprocess_input
from keras.utils import to_categorical
from keras import regularizers
from itertools import product
import os


def create_vgg16_model(input_shape, layer_index=15):
    base_model = vgg16(input_shape, include_top=False, batch_normalization=False)
    for layer in base_model.layers[:layer_index]:
        layer.trainable = False
    for layer in base_model.layers[layer_index:]:
        layer.trainable = True
    x = Flatten()(base_model.output)
    predictions = Dense(2, activation="softmax")(x)
    model_name = "vgg16_full_fc1_aug_frozen_{}_softmax".format(layer_index)
    return model_name, Model(base_model.input, predictions)


def main():
    #project_path = r"/media/megatron/Projects/DeepSolaris"
    project_path = r"/media/tim/Data/Work/CBS/DeepSolaris"
    with Project(project_path=project_path) as project:
        dataset = project.dataset("Heerlen-HR")
        dataset.data = preprocess_input(dataset.data[:,:,:,::-1])

        train_dataset, test_dataset = dataset.split(test_size=0.25)
        class_weights = train_dataset.class_weights

        train_dataset.labels = to_categorical(train_dataset.labels)
        test_dataset.labels = to_categorical(test_dataset.labels)

        train_generator = ImageGenerator(train_dataset)\
                          .with_seed(42)\
                          .with_rotation_range(30)\
                          .with_width_shift_range(0.1)\
                          .with_height_shift_range(0.1)\
                          .with_zoom_range(0.2)\
                          .with_shear_range(0.2)\
                          .with_horizontal_flip(True)\
                          .with_fill_mode("reflect")

        test_generator = ImageGenerator(test_dataset)\
                         .with_seed(84)

        image_shape = dataset.data[0].shape

        name, cnn_model = create_vgg16_model(input_shape=image_shape, layer_index=7)

        model = project.model(name)
        model.create_model(cnn_model)
        model.plot()
        cnn_model.summary()

        #        .with_callbacks([EarlyStopping(patience=5)])\
        with model.run().with_epochs(10)\
                .with_batch_size(64)\
                .with_loss_function("binary_crossentropy")\
                .with_optimizer(RMSPropSettings(lr=1e-5))\
                .with_metric_callbacks([ClassificationReportCallback(), ConfusionMatrixCallback(), PlotRocCallback()])\
                .with_class_weights(class_weights)\
                .with_train_dataset(train_generator)\
                .with_test_dataset(test_generator)\
                .with_evaluation_dataset(test_dataset) as run:
                run.train()
                run.evaluate()


if __name__ == "__main__":
    main()
