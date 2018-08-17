from ProjectPaths import ProjectPaths
from keras.applications import VGG16
import numpy as np

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

model = VGG16()
model.summary()
