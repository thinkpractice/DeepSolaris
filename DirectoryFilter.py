import os


class FileFilter(object):
    def __init__(self, root_path, file_list, file_filter=None):
        self.__root_path = root_path
        self.__file_list = file_list
        self.__filterFunction = file_filter
        if isinstance(file_filter, str):
            self.__filterFunction = lambda filename: file_filter in filename

    @property
    def root_path(self):
        return self.__root_path

    @property
    def files(self):
        return self.filter_files(self.__file_list, self.__filterFunction)

    @property
    def paths(self):
        return self.filter_files(self.__file_list, self.__filterFunction, True)

    @property
    def images(self):
        return FileFilter(self.root_path, self.files, lambda filename: "mask" not in filename)

    @property
    def masks(self):
        return FileFilter(self.root_path, self.files, lambda filename: "mask" in filename and "masked" not in filename)

    @property
    def masked(self):
        return FileFilter(self.root_path, self.files, lambda filename: "masked" in filename)

    def filter_files(self, file_paths, filter_function, include_dir=False):
        return sorted([self.filename_for(filename, include_dir=include_dir) for filename in file_paths if filter_function(filename)])

    def filename_for(self, filename, include_dir=False):
        return os.path.join(self.root_path, filename) if include_dir else filename


class DirectoryFilter(object):
    def __init__(self, root_path):
        self.__root_path = root_path

    @property
    def root_path(self):
        return self.__root_path

    @property
    def all(self):
        return FileFilter(self.root_path, os.listdir(self.root_path), "")

    def __getattr__(self, filter_name):
        return FileFilter(self.root_path, os.listdir(self.root_path), filter_name)

    def dir(self, filter_name):
        sub_path = os.path.join(self.root_path, filter_name)
        if not os.path.exists(sub_path):
            return self
        return DirectoryFilter(sub_path)
