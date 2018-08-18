from ProjectPaths import ProjectPaths
from PerformanceMetrics import PerformanceMetrics
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.callbacks import TensorBoard
from keras.applications.vgg16 import VGG16
from datetime import datetime
import numpy as np
import pandas as pd
import os

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
    return {"vgg16": ""}


def log_dir_for(model_name, batch_size, epochs, lr):
    date = str(datetime.now().date())
    log_dir_name = model_name + "_" + date + "_" + str(batch_size) + "_" + str(epochs) + "_" + str(lr)
    return os.path.join(ProjectPaths.log_dir(),  log_dir_name)

def base_model_for(model_name, pre_trained_weights = "imagenet"):
    return VGG16(weights=pre_trained_weights, include_top=False)

def compile_model(model_name):
    base_model = base_model_for(model_name)
    base_model.summary()
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    for layer in base_model.layers:
        layer.trainable = False
    model.compile(optimizer='rmsprop', loss='binary_crossentropy',
                  metrics=['accuracy', PerformanceMetrics.precision,
                           PerformanceMetrics.recall, PerformanceMetrics.fmeasure])
    return model

def train_model(model_name, model, batch_size, epochs, train_images, train_labels, validation_images, validation_labels, verbose=True):
    log_dir = log_dir_for(model_name, batch_size, epochs, 0)
    tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=0,  write_graph=False, write_images=False)
    model.fit(x = train_images, y = train_labels, epochs = epochs, callbacks= [tensorboard_callback],
              validation_data = (validation_images, validation_labels), batch_size = batch_size,
              verbose = verbose)

def evaluate_model(model_name, model, train_images, train_labels, test_images, test_labels, validation_images, validation_labels):
  train_acc = round(model.evaluate(train_images, train_labels, 128)[1],4)
  valid_acc = round(model.evaluate(validation_images, validation_labels, 128)[1],4)
  test_acc = round(model.evaluate(test_images, test_labels, 128)[1],4)

  print("- Training accuracy:\t{}".format(train_acc))
  print("- Validation accuracy:\t{}".format(valid_acc))
  print("- Test accuracy:\t{}".format(test_acc))
  return model_name, train_acc, test_acc, valid_acc

batch_size = 64
step_size = 420
base_lr = 0.00001
max_lr = 0.001
#epochs = 48
epochs = 1

model_names = models().keys()
model_evaluations = []
for model_name in model_names:
    model = compile_model(model_name)
    train_model(model_name, model, batch_size, epochs, train_images, train_labels, valid_images, valid_labels)
    model_evaluations.append(evaluate_model(model_name, model, train_images, train_labels, test_images, test_labels, valid_images, valid_labels))

evaluation_names = ["model_name", "train_acc", "test_acc", "valid_acc"]
np_model_evaluations = np.array(model_evaluations)
evaluations = pd.DataFrame(np_model_evaluations, index=model_names, columns=evaluation_names)
print(evaluations.head())
