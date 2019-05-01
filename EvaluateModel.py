from keras.models import Model
from keras.layers import GlobalAveragePooling2D, Dense, Dropout, Flatten
from sklearn.metrics import classification_report, confusion_matrix
from cbds.deeplearning.models import vgg16
from sklearn.metrics import roc_curve
import numpy as np
import pandas as pd
import argparse


def find_optimal_cutoff(target, predicted):
    """ Find the optimal probability cutoff point for a classification model related to event rate
    Parameters
    ----------
    target : Matrix with dependent or target data, where rows are observations

    predicted : Matrix with predicted data, where rows are observations

    Returns
    -------
    list type, with optimal cutoff value

    """
    fpr, tpr, threshold = roc_curve(target, predicted)
    i = np.arange(len(tpr))
    roc = pd.DataFrame({'tf' : pd.Series(tpr-(1-fpr), index=i), 'threshold' : pd.Series(threshold, index=i)})
    roc_t = roc.ix[(roc.tf-0).abs().argsort()[:1]]

    return list(roc_t['threshold'])


def get_model(model_path):
    base_model = vgg16(input_shape=(187, 187, 3), include_top=False)
    for layer in base_model.layers:
        layer.trainable = True
    last_conv_layer = base_model.get_layer("block5_pool")
    #x = GlobalAveragePooling2D()(last_conv_layer.output)
    x = Flatten()(last_conv_layer.output)
    x = Dense(512, activation="relu")(x)  # , kernel_regularizer=regularizers.l2(1e-4))(x)
    x = Dropout(0.5)(x)
    #x = Dense(512, activation="relu")(x)
    #x = Dropout(0.5)(x)
    predictions = Dense(1, activation="sigmoid")(x)
    model = Model(base_model.input, predictions)
    model.load_weights(model_path)
    model.summary()
    return model


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--dataset", required=True, help="Path to training set")
    ap.add_argument("-m", "--model_path", required=True, help="Path to model")
    ap.add_argument("-l", "--labels", required=True, help="Path to the labels file")
    args = vars(ap.parse_args())

    print("Loading model...")
    model = get_model(args["model_path"])

    print("Loading data...")
    images = np.load(args["dataset"])
    images = images / 255.
    labels = np.load(args["labels"])
    print("Evaluating data...")
    y_pred = model.predict(images, batch_size=64)
    y_pred = y_pred.reshape(y_pred.shape[0])

    cut_off = find_optimal_cutoff(labels, y_pred)
    predicted_labels = y_pred > cut_off

    print(y_pred.shape)
    print(classification_report(labels, predicted_labels))
    print(confusion_matrix(labels, predicted_labels))


if __name__ == "__main__":
    main()
