from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
import argparse
import pickle
import h5py
import numpy as np


def get_features_for_class(db, data_key, label_key):
    i = int(db[label_key].shape[0] * 0.75)
    return db[data_key][:i], db[label_key][:i], db[data_key][i:], db[label_key][i:]


def shuffle(data, labels):
    idxs = np.arange(0, data.shape[0])
    np.random.shuffle(idxs)
    return data[idxs], labels[idxs]


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--db", required=True, help="path HDF5 database")
ap.add_argument("-m", "--model", required=True, help="path to output model")
ap.add_argument("-j", "--jobs", type=int, default=-1, help="# of jobs to run when tuning hyperparameters")
ap.add_argument("-c", "--classifier", default="lr", help="The classifier to use: logistic regression (lr) or svm")
args = vars(ap.parse_args())

db = h5py.File(args["db"], "r")
positive_train, positive_train_labels, positive_test, positive_test_labels = \
    get_features_for_class(db, "positive_features", "positive_features_labels")
negative_train, negative_train_labels, negative_test, negative_test_labels = \
    get_features_for_class(db, "negative_features", "negative_features_labels")

train_features = np.concatenate((positive_train, negative_train))
train_labels = np.concatenate((positive_train_labels, negative_train_labels))
train_features, train_labels = shuffle(train_features, train_labels)

test_features = np.concatenate((positive_test, negative_test))
test_labels = np.concatenate((positive_test_labels, negative_test_labels))
test_features, test_labels = shuffle(test_features, test_labels)

print("[INFO] tuning hyperparameters...")
params = {"C": [0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0]}
model = GridSearchCV(LogisticRegression(solver="lbfgs", multi_class="auto", class_weight="balanced"), params, cv=3, n_jobs=args["jobs"])
if args["classifier"].lower() == "svm":
    model = GridSearchCV(LinearSVC(class_weight="balanced"), params, cv=3, n_jobs=args["jobs"])

model.fit(train_features, train_labels)
print("[INFO] best hyperparameters: {}".format(model.best_params_))

print("[INFO] evaluating...")
preds = model.predict(test_features)
print(classification_report(test_labels, preds, target_names=db["label_names"]))

print("[INFO] saving model...")
with open(args["model"], "wb") as f:
    f.write(pickle.dumps(model.best_estimator_))

db.close()
