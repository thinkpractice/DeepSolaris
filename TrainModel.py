from ProjectPaths import ProjectPaths
from PerformanceMetrics import PerformanceMetrics
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras.applications.vgg16 import VGG16
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd

train_images = np.load(ProjectPaths.file_in_image_dir('training_images_AcMüDüHo.npy'))
train_labels = np.load(ProjectPaths.file_in_image_dir('training_labels_AcMüDüHo.npy'))

valid_images = np.load(ProjectPaths.file_in_image_dir('validation_images_AcMüDüHo.npy'))
valid_labels = np.load(ProjectPaths.file_in_image_dir('validation_labels_AcMüDüHo.npy'))

test_images = np.load(ProjectPaths.file_in_image_dir('test_images_AcMüDüHo.npy'))
test_labels = np.load(ProjectPaths.file_in_image_dir('test_labels_AcMüDüHo.npy'))


print("Size of:")
print("- Training-set:\t\t{}".format(len(train_labels)))
print("- Validation-set:\t{}".format(len(valid_labels)))
print("- Test-set:\t\t{}".format(len(test_labels)))


def models():
    return {"vgg16": lambda pre_trained_weights, include_top : VGG16(weights=pre_trained_weights, include_top=False) }


def base_model_for(settings):
    model_name = settings["model_name"]
    pre_trained_weights = settings["pre_trained_weights"]
    include_top = settings["include_top"]
    return models()[model_name](pre_trained_weights, include_top)


def compile_model(settings):
    base_model = base_model_for(settings)
    base_model.summary()
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(1, activation='sigmoid')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    all_trainable = settings["all_trainable"]
    for layer in base_model.layers:
        layer.trainable = all_trainable

    model.compile(optimizer='rmsprop', loss='binary_crossentropy',
                  metrics=['accuracy', PerformanceMetrics.precision,
                           PerformanceMetrics.recall, PerformanceMetrics.fmeasure])
    return model


def train_model(model, settings, train_images, train_labels, validation_images,
                validation_labels, verbose=True):
    model_name = settings["model_name"]
    batch_size = settings["batch_size"]
    epochs = settings["epochs"]

    checkpoint_dir = ProjectPaths.checkpoint_dir_for(model_name, batch_size, epochs)
    model_checkpoint_callback = ModelCheckpoint(checkpoint_dir, monitor='val_acc', verbose= verbose,
                                                save_weights_only=True,
                                          save_best_only=True, mode='max', period=1)

    log_dir = ProjectPaths.log_dir_for(model_name, batch_size, epochs, 0)
    tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=0,  write_graph=False, write_images=False)

    model.fit(x=train_images, y=train_labels, epochs=epochs,
              callbacks=[model_checkpoint_callback, tensorboard_callback],
              validation_data=(validation_images, validation_labels), batch_size=batch_size,
              verbose=verbose)


def evaluate_model(model, settings, train_images, train_labels, test_images, test_labels,
                   validation_images, validation_labels):
    model_name = settings["model_name"]
    batch_size = settings["batch_size"]
    train_acc = round(model.evaluate(train_images, train_labels, batch_size)[1],4)
    valid_acc = round(model.evaluate(validation_images, validation_labels, batch_size)[1],4)
    test_acc = round(model.evaluate(test_images, test_labels, batch_size)[1],4)

    #confusion_matrix(true_labels, predicted_labels)

    print(model.metrics_names)
    print("- Training accuracy:\t{}".format(train_acc))
    print("- Validation accuracy:\t{}".format(valid_acc))
    print("- Test accuracy:\t{}".format(test_acc))
    return model_name, train_acc, test_acc, valid_acc


run_settings = {"batch_size": 64,
                "epochs": 1,
                "model_name": "vgg16",
                "pre_trained_weights": "imagenet",
                "include_top": False,
                "all_trainable": False
                }

model_names = models().keys()
model_evaluations = []
for model_name in model_names:
    compiled_model = compile_model(run_settings)
    train_model(compiled_model, run_settings, train_images, train_labels, valid_images, valid_labels)
    model_evaluations.append(evaluate_model(compiled_model, run_settings, train_images, train_labels, test_images, test_labels, valid_images, valid_labels))

evaluation_names = ["model_name", "train_acc", "test_acc", "valid_acc"]
np_model_evaluations = np.array(model_evaluations)
evaluations = pd.DataFrame(np_model_evaluations, index=model_names, columns=evaluation_names)
print(evaluations.head())
