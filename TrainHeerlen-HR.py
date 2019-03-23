from cbds.deeplearning.models import vgg16
from keras.models import Model
from keras.layers import GlobalAveragePooling2D, Dense, Dropout, Flatten
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, TensorBoard, EarlyStopping
from keras.optimizers import SGD
from ProjectPaths import ProjectPaths
from PerformanceMetrics import PerformanceMetrics
from datetime import datetime
from sklearn.metrics import classification_report, confusion_matrix
import os
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def get_model():
    base_model = vgg16(input_shape=(187, 187, 3), include_top=False)
    for layer in base_model.layers:
        layer.trainable = True
    last_conv_layer = base_model.get_layer("block4_pool")
    #x = GlobalAveragePooling2D()(last_conv_layer.output)
    x = Flatten()(last_conv_layer.output)
    x = Dense(512, activation="relu")(x)  # , kernel_regularizer=regularizers.l2(1e-4))(x)
    x = Dropout(0.5)(x)
    x = Dense(512, activation="relu")(x)
    x = Dropout(0.5)(x)
    predictions = Dense(1, activation="sigmoid")(x)
    model = Model(base_model.input, predictions)
    model.summary()
    return model


def plot_loss_and_acc(H, epochs_ran):
    matplotlib.use("Agg")
    _, ax = plt.subplots(1, 2, figsize=(25, 10))
    ax[0].plot(np.arange(0, epochs_ran), H.history["acc"], label="accuracy")
    ax[0].plot(np.arange(0, epochs_ran), H.history["val_acc"], label="val_accuracy", color="r")
    ax[0].set_xlim([0, epochs_ran])
    ax[1].plot(np.arange(0, epochs_ran), H.history["loss"], label="loss", color="g")
    ax[1].plot(np.arange(0, epochs_ran), H.history["val_loss"], label="val_loss", color="y")
    ax[1].set_xlim([0, epochs_ran])
    ax[0].legend()
    ax[1].legend()
    ax[0].set_ylabel("Loss/Accuracy")
    ax[0].set_xlabel("Epochs")
    ax[1].set_ylabel("Loss/Accuracy")
    ax[1].set_xlabel("Epochs")
    plt.show()
    plt.savefig("loss_accuracy_{}.png".format(datetime.now().strftime("%d-%m-%Y_%H:%M:%S")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--dataset", required=True, help="Path to training set")
    ap.add_argument("-v", "--valset", required=True, help="Path to validation set")
    ap.add_argument("-l", "--labels", required=True, help="Path to the labels file")
    ap.add_argument("-a", "--vallabels", required=True, help="Path to the validation labels file")
    ap.add_argument("-e", "--epochs", default=30, type=int, help="Number of epochs to train the network")
    ap.add_argument("-b", "--batch-size", default=64, type=int, help="Batch size")
    ap.add_argument("-r", "--learning-rate", default=0.0001, type=float, help="Learning rate for the optimizer")
    ap.add_argument("-m", "--momentum", default=0.9, type=float, help="Momentum")
    args = vars(ap.parse_args())

    batch_size = args["batch_size"]
    epochs = args["epochs"]
    learning_rate = args["learning_rate"]
    decay_rate = learning_rate / epochs
    momentum = args["momentum"]

    sgd = SGD(lr=learning_rate, momentum=momentum, decay=decay_rate, nesterov=True)

    data_generator = ImageDataGenerator(rescale=1/255.,
                                        rotation_range=20,
                                        width_shift_range=0.2,
                                        height_shift_range=0.2,
                                        channel_shift_range=0.1,
                                        zoom_range=0.3,
                                        shear_range=0.15,
                                        horizontal_flip=True,
                                        fill_mode="nearest")

    test_generator = ImageDataGenerator(rescale=1/255.)

    train_images = np.load(args["dataset"])
    train_labels = np.load(args["labels"])
    test_images = np.load(args["valset"])
    test_labels = np.load(args["vallabels"])

    train_generator = data_generator.flow(train_images, train_labels, batch_size=batch_size)
    test_generator = test_generator.flow(test_images, test_labels)
    class_weights = {
        0: 1.,
        1: train_labels[train_labels == 0].size / train_labels[train_labels == 1].size
    }

    model = get_model()
    model.compile(sgd, loss="binary_crossentropy", metrics=['accuracy', PerformanceMetrics.precision,
                  PerformanceMetrics.recall, PerformanceMetrics.fmeasure])

    model_name = "vgg16_heerlen_hr_batch_norm_{}".format(datetime.now().strftime("%d-%m-%Y_%H:%M:%S"))

    checkpoint_dir = ProjectPaths.instance().checkpoint_dir_for(model_name, batch_size, epochs)
    if not os.path.exists(checkpoint_dir):
        os.mkdir(checkpoint_dir)

    file_in_checkpoint_dir = ProjectPaths.instance().file_in_checkpoint_dir(model_name, batch_size,
                                                                            epochs,  model_name +
                                                                            "__{epoch:02d}_{val_acc:.2f}.hdf5")

    early_stopping_callback = EarlyStopping(monitor='val_acc', patience=5)
    model_checkpoint_callback = ModelCheckpoint(file_in_checkpoint_dir, monitor='val_acc', verbose=True,
                                                save_weights_only=True,
                                                save_best_only=True)

    log_dir = os.path.join(ProjectPaths.instance().log_dir, model_name)
    tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=0,  write_graph=False, write_images=False)

    train_history = model.fit_generator(train_generator,
                            steps_per_epoch=len(train_labels) // batch_size,
                            epochs=epochs,
                            callbacks=[early_stopping_callback, model_checkpoint_callback, tensorboard_callback],
                            validation_data=test_generator,
                            validation_steps=len(test_labels) // batch_size,
                            class_weight=class_weights)

    epochs_ran = len(train_history.history["loss"])
    plot_loss_and_acc(train_history, epochs_ran)

    y_pred = model.predict(test_images)
    print(classification_report(test_labels, y_pred.round()))
    print(confusion_matrix(test_labels, y_pred.round()))


if __name__ == "__main__":
    main()
