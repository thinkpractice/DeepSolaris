from ProjectPaths import ProjectPaths
from PerformanceMetrics import PerformanceMetrics
from ModelFactory import ModelFactory
from Datasets import Datasets
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras.optimizers import SGD, RMSprop
from sklearn.metrics import confusion_matrix
from collections import namedtuple
import numpy as np
import pandas as pd
import csv
import sys

RunSettings = namedtuple("RunSettings", ["model_name", "pre_trained_weights", "include_top", "all_trainable",
                                         "dataset_name", "batch_size", "epochs", "optimizer", "lr",
                                         "momentum", "decay", "nesterov"])


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
    file_in_checkpoint_dir = ProjectPaths.file_in_checkpoint_dir(settings.model_name, settings.batch_size,
                                                                 settings.epochs, "{}__{epoch:02d}_{val_acc:.2f}.hdf5"
                                                                 .format(settings.model_name))

    model_checkpoint_callback = ModelCheckpoint(file_in_checkpoint_dir, monitor='val_acc', verbose=verbose,
                                                save_weights_only=True,
                                                save_best_only=True)
    log_dir = ProjectPaths.log_dir_for(settings.model_name, settings.batch_size, settings.epochs, settings.lr)
    tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=0,  write_graph=False, write_images=False)

    model.fit(x=train_images, y=train_labels, epochs=settings.epochs,
              callbacks=[model_checkpoint_callback, tensorboard_callback],
              validation_data=(validation_images, validation_labels), batch_size=settings.batch_size,
              verbose=verbose)


def evaluate_model(model, settings, datasets):
    column_headers = list(settings._fields)
    column_values = list(settings)

    for dataset in datasets:
        column_headers.extend(["{}_{}".format(dataset.name, metric_name) for metric_name in model.metrics_names])
        column_values.extend(model.evaluate(dataset.images, dataset.labels, settings.batch_size))

        column_headers.extend(["{}_{}".format(dataset.name, confusion_label) for confusion_label in ["tn", "fp", "fn",
                                                                                                     "tp"]])
        # Confusion matrix assumes sigmoid cut-off at 0.5, below is negative, above is positive
        predicted_labels = [np.round(prediction) for prediction in model.predict(dataset.images)]
        column_values.extend(confusion_matrix(dataset.labels, predicted_labels).ravel())

    return column_headers, column_values


def train_and_evaluate(run_settings_list):
    for run_settings in run_settings_list:
        model = ModelFactory.model_for(run_settings)
        compiled_model = compile_model(model, run_settings)

        dataset = Datasets.dataset_for(run_settings.dataset_name)
        train_model(compiled_model, run_settings, dataset[0].images, dataset[0].labels, dataset[2].images, dataset[2].labels)

        headers, values = evaluate_model(compiled_model, run_settings, dataset)
        yield run_settings.model_name, headers, values


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

            run_names.append(run_name)
            column_headers.append(header)
            model_evaluations.append(evaluations)
    return run_names, column_headers, np.array(model_evaluations)


def load_run_settings(filename):
    return [RunSettings(model_name="vgg16", pre_trained_weights="imagenet", include_top=False, all_trainable=False,
                        dataset_name="AcMüDüHo", batch_size=64, epochs=1, optimizer="rmsprop", lr=None, momentum=None,
                        decay=None, nesterov=None) for _ in range(1)]


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


