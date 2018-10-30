from datetime import datetime
import os
import socket

class ProjectPaths(object):
    project_paths_instance = None
    base_dirs = {"tim-Z370-AORUS-Gaming-7":  r"/media/tim/Data/Work/CBS/DeepSolaris",
                 "gebruiker-HP-EliteBook-840-G5": r"/home/tdjg/Documents/DeepSolaris",
                 }

    def __init__(self, base_dir):
        self.__base_dir = base_dir

    @classmethod
    def base_dir_for_machine(self):
        return self.base_dirs[socket.gethostname()]

    @classmethod
    def instance(cls, base_dir=None):
        if not base_dir:
            base_dir = cls.base_dir_for_machine()
        if not cls.project_paths_instance:
            cls.project_paths_instance = ProjectPaths(base_dir)
        return cls.project_paths_instance

    @property
    def base_dir(self):
        return self.__base_dir

    @property
    def image_dir(self):
        return os.path.join(self.base_dir, "Images")

    @property
    def model_dir(self):
        return os.path.join(self.base_dir, "Models")

    @property
    def log_dir(self):
        return os.path.join(self.base_dir, "Logs")

    def file_in_base_dir(self, filename):
        return os.path.join(self.base_dir, filename)

    def file_in_image_dir(self, filename):
        return os.path.join(self.image_dir, filename)

    def log_dir_for(self, model_name, batch_size, epochs, lr):
        date = str(datetime.now().date())
        learning_rate = "default_lr" if not lr else str(lr)
        log_dir_name = model_name + "_" + date + "_" + str(batch_size) + "_" + str(epochs) + "_" + learning_rate
        return os.path.join(self.log_dir,  log_dir_name)

    def checkpoint_dir_for(self, model_name, batch_size, epochs):
        date = str(datetime.now().date())
        check_point_dir = model_name + "_" + date + "_" + str(batch_size) + "_" + str(epochs)
        return os.path.join(self.model_dir, check_point_dir)

    def logfile_in_log_dir(self, filename_template):
        filename = filename_template.format(datetime.now().strftime("%Y%m%d_%H:%M:%S"))
        return os.path.join(self.log_dir, filename)

    def file_in_checkpoint_dir(self, model_name, batch_size, epochs, filename_template):
        checkpoint_dir = self.checkpoint_dir_for(model_name, batch_size, epochs)
        return os.path.join(checkpoint_dir, filename_template)
