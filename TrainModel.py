from ProjectPaths import ProjectPaths
from PerformanceMetrics import PerformanceMetrics
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.callbacks import TensorBoard
from keras.applications.vgg16 import VGG16
from datetime import datetime
import numpy as np
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


def log_dir_for(model_name, batch_size, epochs, lr):
    date = str(datetime.now().date())
    log_dir_name = model_name + "_" + date + "_" + batch_size + "_" + epochs + "_" + lr
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

def evaluate_model(model_name, model):
    pass


batch_size = 64
step_size = 420
base_lr = 0.00001
max_lr = 0.001
epochs = 48

model_name = "vgg16"
model = compile_model(model_name)
train_model(model_name, model, batch_size, epochs, train_images, test_labels, valid_images, valid_labels)
