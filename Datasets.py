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
        return Datasets.load_data(ProjectPaths.instance().file_in_image_dir(filename))

    @classmethod
    def available_datasets(cls):
        return Datasets.datasets().keys()

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
                                           labels=Datasets.load_image_data('test_labels_AcMüDüHo.npy'))],
                "Bradbury": [Datasets.EvaluationSet(name="train",
                                           images=Datasets.load_image_data('train_images_Bradbury.npy'),
                                           labels=Datasets.load_image_data('train_labels_Bradbury.npy')),
                             #Datasets.EvaluationSet(name="test",
                             #              images=Datasets.load_image_data('validation_images_Bradbury.npy'),
                             #              labels=Datasets.load_image_data('validation_labels_Bradbury.npy')),
                             Datasets.EvaluationSet(name="validation",
                                           images=Datasets.load_image_data('test_images_Bradbury.npy'),
                                           labels=Datasets.load_image_data('test_labels_Bradbury.npy'))],
                "Fresno":   [Datasets.EvaluationSet(name="train",
                                           images=Datasets.load_image_data('train_images_Fresno.npy'),
                                           labels=Datasets.load_image_data('train_labels_Fresno.npy')),
                             #Datasets.EvaluationSet(name="test",
                             #              images=Datasets.load_image_data('validation_images_Fresno.npy'),
                             #              labels=Datasets.load_image_data('validation_labels_Fresno.npy')),
                             Datasets.EvaluationSet(name="validation",
                                           images=Datasets.load_image_data('test_images_Fresno.npy'),
                                           labels=Datasets.load_image_data('test_labels_Fresno.npy'))],
                "CBS":      [Datasets.EvaluationSet(name="train",
                                           images=Datasets.load_image_data('train_images_CBS.npy'),
                                           labels=Datasets.load_image_data('train_labels_CBS.npy')),
                             #Datasets.EvaluationSet(name="test",
                             #              images=Datasets.load_image_data('validation_images_CBS.npy'),
                             #              labels=Datasets.load_image_data('validation_labels_CBS.npy')),
                             Datasets.EvaluationSet(name="validation",
                                           images=Datasets.load_image_data('test_images_CBS.npy'),
                                           labels=Datasets.load_image_data('test_labels_CBS.npy'))]
                }

    @classmethod
    def dataset_for(cls, dataset_name):
        return Datasets.datasets()[dataset_name]


