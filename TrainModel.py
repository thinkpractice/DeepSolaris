from ProjectPaths import ProjectPaths
from PerformanceMetrics import PerformanceMetrics
from ModelFactory import ModelFactory
from Datasets import Datasets
from keras.callbacks import ModelCheckpoint, TensorBoard, EarlyStopping
from keras.optimizers import SGD, RMSprop
from sklearn.metrics import confusion_matrix
from collections import namedtuple
import numpy as np
import pandas as pd
import csv
import sys
import os

RunSettings = namedtuple("RunSettings", ["model_name", "last_vgg_layer", "pre_trained_weights", "include_top", "all_trainable",
                                         "dataset_name", "batch_size", "epochs", "optimizer", "lr",
                                         "momentum", "decay", "nesterov"])

def run_name_for(settings):
    return "{}_pr_{}_al_{}_{}_e_{}_bs_{}_op_{}".format(settings.model_name, settings.pre_trained_weights,
                                                       settings.all_trainable, settings.dataset_name, settings.epochs,
                                                       settings.batch_size, settings.optimizer)

def optimizers():
    return {"sgd": lambda settings: SGD(settings.lr, settings.momentum, settings.decay, settings.nesterov),
            "rmsprop": lambda settings: RMSprop(settings.lr) if settings.lr else RMSprop()}


def optimizer_for(settings):
    return optimizers()[settings.optimizer](settings)


def compile_model(model, settings):
    model.compile(optimizer=optimizer_for(settings), loss='binary_crossentropy',
                  metrics=['accuracy', PerformanceMetrics.precision,
                           PerformanceMetrics.recall, PerformanceMetrics.fmeasure])
    return model


def train_model(model, settings, train_images, train_labels, validation_images, validation_labels, verbose=True):
    checkpoint_dir = ProjectPaths.checkpoint_dir_for(run_name_for(settings), settings.batch_size, settings.epochs)
    if not os.path.exists(checkpoint_dir):
        os.mkdir(checkpoint_dir)

    file_in_checkpoint_dir = ProjectPaths.file_in_checkpoint_dir(run_name_for(settings), settings.batch_size,
                                                                 settings.epochs, settings.model_name +
                                                                 "__{epoch:02d}_{val_acc:.2f}.hdf5")

    early_stopping_callback = EarlyStopping(patience=10)
    model_checkpoint_callback = ModelCheckpoint(file_in_checkpoint_dir, monitor='val_acc', verbose=verbose,
                                                save_weights_only=True,
                                                save_best_only=True)
    log_dir = os.path.join(ProjectPaths.log_dir(), run_name_for(settings))
    tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=0,  write_graph=False, write_images=False)

    model.fit(x=train_images, y=train_labels, epochs=settings.epochs,
              callbacks=[early_stopping_callback, model_checkpoint_callback, tensorboard_callback],
              validation_data=(validation_images, validation_labels), batch_size=settings.batch_size,
              verbose=verbose)


def evaluate_model(model, settings, datasets):
    column_headers = list(settings._fields)
    column_values = list(settings)

    cut_offs = [0.1 + 0.1 * i for i in range(8)]
    for dataset in datasets:
        column_headers.extend(["{}_{}".format(dataset.name, metric_name) for metric_name in model.metrics_names])
        column_values.extend(model.evaluate(dataset.images, dataset.labels, settings.batch_size))

        for cut_off in cut_offs:
            column_headers.extend(["{}_{}_{}".format(dataset.name, cut_off, confusion_label)
                                   for confusion_label in ["tn", "fp", "fn", "tp"]])
            # Calculates confusion matrices for different cut-off at values
            predicted_labels = [prediction < cut_off
                                for prediction in model.predict(dataset.images)]
            column_values.extend(confusion_matrix(dataset.labels, predicted_labels).ravel())

    return column_headers, column_values


def train_and_evaluate(run_settings_list):
    for run_settings in run_settings_list:
        run_name = run_name_for(run_settings)
        print("Training and evaluating: {}".format(run_name))
        model = ModelFactory.model_for_settings(run_settings)
        compiled_model = compile_model(model, run_settings)

        dataset = Datasets.dataset_for(run_settings.dataset_name)
        train_model(compiled_model, run_settings, dataset[0].images, dataset[0].labels, dataset[2].images, dataset[2].labels)

        headers, values = evaluate_model(compiled_model, run_settings, dataset)
        yield run_name, headers, values


def train_evaluate_and_log(csv_filename, run_settings_list):
    write_header_row = True
    run_names = []
    column_headers = []
    model_evaluations = []
    with open(csv_filename, "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")
        for run_name, header, evaluations in train_and_evaluate(run_settings_list):
            if write_header_row:
                csv_writer.writerow(header)
                write_header_row = False
            values = [run_name]
            values.extend(evaluations)
            csv_writer.writerow(values)
            csv_file.flush()

            run_names.append(run_name)
            column_headers.append(header)
            model_evaluations.append(evaluations)
    return run_names, column_headers, np.array(model_evaluations)


def load_run_settings(filename):
    return [RunSettings(model_name="vgg16_gap", last_vgg_layer=last_layer, pre_trained_weights=weights, include_top=False, all_trainable=all_trainable,
                        dataset_name=dataset, batch_size=batch_size, epochs=epochs, optimizer="rmsprop",
                        lr=None, momentum=None,
                        decay=None, nesterov=None)
            for last_layer in ["block2_conv2", "block3_conv3", "block4_conv3", "block5_conv3"]
            for dataset in list(Datasets.available_datasets())[:-1]
            for weights in ["imagenet"]
            for all_trainable in [False]
            for epochs in [200]
            for batch_size in [64]
            ]

# [RunSettings(model_name=model, last_vgg_layer="", pre_trained_weights=weights, include_top=False, all_trainable=all_trainable,
#                         dataset_name=dataset, batch_size=batch_size, epochs=epochs, optimizer="rmsprop",
#                         lr=None, momentum=None,
#                         decay=None, nesterov=None)
#             for model in ["vgg16", "vgg19", "xception", "resnet50"] #ModelFactory.available_base_models()
#             for dataset in list(Datasets.available_datasets())[:-1]
#             for weights in ["imagenet", None]
#             for all_trainable in [False, True]
#             for epochs in [200]
#             for batch_size in [64]
#             ]

def main(argv):
    if len(argv) <= 1:
        print("Usage: TrainModel.py <run settings filename>")
        exit(0)

    run_settings_list = load_run_settings(argv[1])
    print(run_settings_list)

    csv_filename = ProjectPaths.logfile_in_log_dir("all_runs_{}.csv")
    run_names, column_headers, np_model_evaluations = train_evaluate_and_log(csv_filename, run_settings_list)

    evaluations = pd.DataFrame(np_model_evaluations, index=run_names, columns=column_headers)
    print(evaluations.head())


if __name__ == "__main__":
    main(sys.argv)


