import os


class FileFilter(object):
    def __init__(self, file_list, filter_name=""):
        self.__file_list = file_list
        self.__filter = filter_name

    @property
    def files(self):
        return self.filter_files(self.__file_list, lambda filename: self.__filter in filename)

    @property
    def images(self):
        return self.filter_files(self.files, lambda filename: "mask" not in filename)

    @property
    def masks(self):
        return self.filter_files(self.files, lambda filename: "mask" in filename and "masked" not in filename)

    @property
    def masked(self):
        return self.filter_files(self.files, lambda filename: "masked" in filename)

    @staticmethod
    def filter_files(file_paths, filter_function):
        return sorted([filename for filename in file_paths if filter_function(filename)])


class DirectoryFilter(object):
    def __init__(self, root_path):
        self.__root_path = root_path

    @property
    def root_path(self):
        return self.__root_path

    @property
    def all(self):
        return FileFilter(os.listdir(self.root_path), "")

    def __getattr__(self, filter_name):
        return FileFilter(os.listdir(self.root_path), filter_name)

    def dir(self, filter_name):
        sub_path = os.path.join(self.root_path, filter_name)
        if not os.path.exists(sub_path):
            return self
        return DirectoryFilter(sub_path)
