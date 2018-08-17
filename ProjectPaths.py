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