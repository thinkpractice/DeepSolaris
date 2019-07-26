from cbds.deeplearning import Project, ImageGenerator
from cbds.deeplearning.metrics import ClassificationReportCallback, ConfusionMatrixCallback, PlotRocCallback
from cbds.deeplearning.settings import RMSPropSettings
from cbds.deeplearning.models import vgg16
from keras.models import load_model, Model
from keras.layers import Flatten, Dense
from keras import regularizers
import argparse
import os


def create_vgg16_model(input_shape, layer_index=7):
    base_model = vgg16(input_shape, include_top=False, batch_normalization=False)
    for layer in base_model.layers[:layer_index]:
        layer.trainable = False
    for layer in base_model.layers[layer_index:]:
        layer.trainable = True
    x = Flatten()(base_model.output)
    predictions = Dense(1, activation="sigmoid", kernel_regularizer=regularizers.l2(0.01))(x)
    model_name = "vgg16_full_fc1_aug_frozen_rms_prop_l2_0.01"
    return model_name, Model(base_model.input, predictions)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project-path", default=r"/media/megatron/Projects/DeepSolaris", help="The project path to use")
    parser.add_argument("-d", "--training-set", required=True, help="The dataset to train on")
    parser.add_argument("-t", "--test-set", required=True, help="The dataset to test on")
    parser.add_argument("-v", "--validation-set", required=True, help="The dataset to validate on")
    parser.add_argument("-s", "--sample-size", required=True, type=float, help="The sample fraction of the training set")
    parser.add_argument("-e", "--epochs", default=10, type=int, help="The number of epochs to train the model")
    parser.add_argument("-b", "--batch_size", default=32, type=int, help="The batch_size to train with")
    parser.add_argument("-l", "--learning_rate", default=1e-4, type=float, help="The learning rate to train with")
    #parser.add_argument("-m", "--model-filename", required=True, help="The model to evaluate")
    #parser.add_argument("-n", "--model-name", required=True, help="The name of the model to evaluate")
    args = vars(parser.parse_args())

    with Project(project_path=args["project_path"]) as project:
        dataset = project.dataset(args["training_set"])
        dataset.data = dataset.data[:, :, :, ::-1]
        train_dataset = dataset.sample(sample_size=args["sample_size"], random_state=42)
        test_dataset = project.dataset(args["test_set"])
        validation_dataset = project.dataset(args["validation_set"])

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

        validation_generator = ImageGenerator(validation_dataset)\
                                .with_rescale(1/255.)\
                                .with_seed(84)

        #model_name, cnn_model = load_model(args["model_filename"])
        model_name, cnn_model = create_vgg16_model(input_shape=(187, 187, 3))
        model = project.model("{}_{}".format(model_name, str(args["sample_size"])))
        model.create_model(cnn_model)
        model.plot()
        cnn_model.summary()

        with model.run().with_epochs(args["epochs"])\
                .with_batch_size(args["batch_size"])\
                .with_loss_function("binary_crossentropy")\
                .with_optimizer(RMSPropSettings(lr=args["learning_rate"]))\
                .with_metric_callbacks([ClassificationReportCallback(), ConfusionMatrixCallback(), PlotRocCallback()])\
                .with_class_weights(train_dataset.class_weights)\
                .with_train_dataset(train_generator)\
                .with_test_dataset(test_generator)\
                .with_evaluation_dataset(test_generator)\
                .with_evaluation_dataset(validation_generator) as run:
                run.train()
                run.evaluate()


if __name__ == "__main__":
    main()
