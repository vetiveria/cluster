"""
Module directories
"""
import os

import config


class Directories:
    """
    Class Directories: Preparing directories
    """

    def __init__(self):
        """
        The constructor
        """
        self.paths = [config.parent, config.data_path, config.warehouse, config.path_matrix,
                      config.path_principals, config.path_principals_attributes, config.path_clusters]

    def cleanup(self):
        """
        Clears the directories for archived & de-archived data

        :return: None
        """

        # Foremost, delete files
        for path in self.paths:
            files_ = [os.remove(os.path.join(base, file))
                      for base, _, files in os.walk(path) for file in files]

            if any(files_):
                raise Exception('Unable to delete all files within path {}'.format(path))

        # ... then, directories
        for path in self.paths:
            directories_ = [os.removedirs(os.path.join(base, directory))
                            for base, directories, _ in os.walk(path, topdown=False) for directory in directories
                            if os.path.exists(os.path.join(base, directory))]

            if any(directories_):
                raise Exception('Unable to delete all directories within path {}'.format(path))

    def create(self):
        """
        Creates directories for (a) archived files, (b) de-archived files

        :return: None
        """

        for path in self.paths:
            if not os.path.exists(path):
                os.makedirs(path)

    def exc(self):
        """
        Entry point
        :return:
        """

        self.cleanup()
        self.create()
