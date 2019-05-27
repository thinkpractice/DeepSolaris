from sklearn.model_selection import RandomizedSearchCV
from cbds.deeplearning import Project, ImageGenerator
from cbds.deeplearning import ImageGenerator
from cbds.deeplearning.settings import SGDSettings
from cbds.deeplearning.models.vgg16 import vgg16
from cbds.deeplearning.metrics import ClassificationReportCallback, ConfusionMatrixCallback, PlotRocCallback
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from itertools import product
import os


def train_model_until(model, layer_index=15):
    for layer in model.layers[:layer_index]:
        layer.trainable = False
    for layer in model.layers[layer_index:]:
        layer.trainable = True
    model_name = "vgg16_rmsprop_fine_tune_sgd"
    return model_name, model


def main():
    #project_path = r"/media/megatron/Projects/DeepSolaris"
    project_path = r"/media/tim/Data/Work/CBS/DeepSolaris"
    with Project(project_path=project_path) as project:
        dataset = project.dataset("Heerlen-HR")
        dataset.data = dataset.data[:,:,:,::-1]

        train_dataset, test_dataset = dataset.split(test_size=0.2)

        train_generator = ImageGenerator(train_dataset)\
                          .with_rescale(1/255.)\
                          .with_rotation_range(30)\
                          .with_width_shift_range(0.1)\
                          .with_height_shift_range(0.1)\
                          .with_zoom_range(0.2)\
                          .with_shear_range(0.2)\
                          .with_horizontal_flip(True)\
                          .with_fill_mode("reflect")

        test_generator = ImageGenerator(test_dataset)\
                         .with_rescale(1/255.)

        image_shape = dataset.data[0].shape


        name = "vgg16_rmsprop_fine_tune_sgd"
        model = project.model(name)
        model.import_model(r"/media/tim/Data/Work/CBS/DeepSolaris/models/vgg16_full_fc512_fc512_fc1_aug_frozen_rms_prop/runs/2019/5/25/11:56:19/model.hdf5")

        model.plot()
        name, cnn_model = train_model_until(model.model)
        cnn_model.summary()

        epochs = 15
        lr = 1e-2
        decay = lr / epochs
        #        .with_callbacks([EarlyStopping(patience=5)])\
        with model.run().with_epochs(epochs)\
                .with_batch_size(64)\
                .with_loss_function("binary_crossentropy")\
                .with_optimizer(SGDSettings(lr=lr, momentum=0.9, decay=decay, nesterov=False))\
                .with_metric_callbacks([ClassificationReportCallback(), ConfusionMatrixCallback(), PlotRocCallback()])\
                .with_class_weights(train_dataset.class_weights)\
                .with_train_dataset(train_generator)\
                .with_test_dataset(test_generator)\
                .with_evaluation_dataset(test_generator) as run:
                run.train()
                run.evaluate()


if __name__ == "__main__":
    main()
