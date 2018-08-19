from ProjectPaths import ProjectPaths
from PerformanceMetrics import PerformanceMetrics
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras.applications.vgg16 import VGG16
from keras.optimizers import SGD, RMSprop
from sklearn.metrics import confusion_matrix
from collections import namedtuple
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

RunSettings = namedtuple("RunSettings", ["model_name", "pre_trained_weights", "include_top", "all_trainable", "batch_size", "epochs", "optimizer", "lr", "momentum", "decay", "nesterov"])
EvaluationSet = namedtuple("EvaluationSet", ["name", "images", "labels"])


def models():
    return {"vgg16": lambda pre_trained_weights, include_top: VGG16(weights=pre_trained_weights, include_top=False)}


def optimizers():
    return {"sgd": lambda settings: SGD(settings.lr, settings.momentum, settings.decay, settings.nesterov),
            "rmsprop": lambda settings: RMSprop(settings.lr) if settings.lr else RMSprop()}


def base_model_for(settings):
    return models()[settings.model_name](settings.pre_trained_weights, settings.include_top)


def optimizer_for(settings):
    return optimizers()[settings.optimizer](settings)


def compile_model(settings):
    base_model = base_model_for(settings)
    base_model.summary()
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(1, activation='sigmoid')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    for layer in base_model.layers:
        layer.trainable = settings.all_trainable

    model.compile(optimizer=optimizer_for(settings), loss='binary_crossentropy',
                  metrics=['accuracy', PerformanceMetrics.precision,
                           PerformanceMetrics.recall, PerformanceMetrics.fmeasure])
    return model


def train_model(model, settings, train_images, train_labels, validation_images,
                validation_labels, verbose=True):
    checkpoint_dir = ProjectPaths.checkpoint_dir_for(settings.model_name, settings.batch_size, settings.epochs)
    model_checkpoint_callback = ModelCheckpoint(checkpoint_dir, monitor='val_acc', verbose=verbose,
                                                save_weights_only=True,
                                                save_best_only=True, mode='max', period=1)

    log_dir = ProjectPaths.log_dir_for(settings.model_name, settings.batch_size, settings.epochs, 0)
    tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=0,  write_graph=False, write_images=False)

    model.fit(x=train_images, y=train_labels, epochs=settings.epochs,
              callbacks=[model_checkpoint_callback, tensorboard_callback],
              validation_data=(validation_images, validation_labels), batch_size=settings.batch_size,
              verbose=verbose)


def evaluate_model(model, settings, train_images, train_labels, test_images, test_labels,
                   validation_images, validation_labels):
    column_headers=list(settings._fields)
    column_values=list(settings)

    datasets = [EvaluationSet(name="train", images=train_images, labels=train_labels),
                EvaluationSet(name="test", images=test_images, labels=test_labels),
                EvaluationSet(name="validation", images=valid_images, labels=valid_labels)
                ]

    for dataset in datasets:
        column_headers.extend(["{}_{}".format(dataset.name, metric_name) for metric_name in model.metrics_names])
        column_values.extend(model.evaluate(dataset.images, dataset.labels, settings.batch_size))

    #confusion_matrix(true_labels, predicted_labels)

    return column_headers, column_values


def train_and_evaluate(run_settings_list):
    run_names = []
    column_headers = []
    model_evaluations = []
    for run_settings in run_settings_list:
        compiled_model = compile_model(run_settings)
        train_model(compiled_model, run_settings, train_images, train_labels, valid_images, valid_labels)
        run_names.append(run_settings.model_name)
        headers, values = evaluate_model(compiled_model, run_settings, train_images, train_labels, test_images,
                                         test_labels,valid_images, valid_labels)
        column_headers = headers
        model_evaluations.append(values)

    return run_names, column_headers, np.array(model_evaluations)


run_settings = RunSettings(model_name="vgg16", pre_trained_weights="imagenet", include_top=False, all_trainable=False,
                           batch_size=64, epochs=1, optimizer="rmsprop", lr=None, momentum=None, decay=None,
                           nesterov=None)
run_names, column_headers, np_model_evaluations = train_and_evaluate([run_settings])

evaluation_names = ["model_name", "train_acc", "test_acc", "valid_acc"]
evaluations = pd.DataFrame(np_model_evaluations, index=run_names, columns=column_headers)
print(evaluations.head())
