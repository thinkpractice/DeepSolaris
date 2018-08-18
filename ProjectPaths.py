from datetime import datetime
import os

class ProjectPaths(object):
    @classmethod
    def base_dir(cls):
        return r"/media/tim/Data/Work/CBS/Code_hannah"

    @classmethod
    def image_dir(cls):
        return os.path.join(ProjectPaths.base_dir(), "Images")

    @classmethod
    def file_in_image_dir(cls, filename):
        return os.path.join(ProjectPaths.image_dir(), filename)

    @classmethod
    def model_dir(cls):
        return os.path.join(ProjectPaths.base_dir(), "Models")

    @classmethod
    def log_dir(cls):
        return os.path.join(ProjectPaths.base_dir(), "Logs")

    @classmethod
    def log_dir_for(cls, model_name, batch_size, epochs, lr):
        date = str(datetime.now().date())
        log_dir_name = model_name + "_" + date + "_" + str(batch_size) + "_" + str(epochs) + "_" + str(lr)
        return os.path.join(ProjectPaths.log_dir(),  log_dir_name)

    @classmethod
    def checkpoint_dir_for(cls, model_name, batch_size, epochs):
        date = str(datetime.now().date())
        check_point_dir = model_name + "_" + date + "_" + str(batch_size) + "_" + str(epochs)
        return os.path.join(ProjectPaths.model_dir(), check_point_dir)
