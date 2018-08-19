from collections import namedtuple
from ProjectPaths import ProjectPaths
import numpy as np

class Datasets(object):
    EvaluationSet = namedtuple("EvaluationSet", ["name", "images", "labels"])

    @classmethod
    def load_data(cls, filename):
        return np.load(filename)

    @classmethod
    def load_image_data(cls, filename):
        return Datasets.load_data(ProjectPaths.file_in_image_dir(filename))

    @classmethod
    def datasets(cls):
        return {"AcMüDüHo": [Datasets.EvaluationSet(name="train",
                                           images=Datasets.load_image_data('training_images_AcMüDüHo.npy'),
                                           labels=Datasets.load_image_data('training_labels_AcMüDüHo.npy')),
                             Datasets.EvaluationSet(name="test",
                                           images=Datasets.load_image_data('validation_images_AcMüDüHo.npy'),
                                           labels=Datasets.load_image_data('validation_labels_AcMüDüHo.npy')),
                             Datasets.EvaluationSet(name="validation",
                                           images=Datasets.load_image_data('test_images_AcMüDüHo.npy'),
                                           labels=Datasets.load_image_data('test_labels_AcMüDüHo.npy'))]
                }

    @classmethod
    def dataset_for(cls, dataset_name):
        return Datasets.datasets()[dataset_name]


