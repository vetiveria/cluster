"""
This module creates a design matrix via the data files of data/data/
using the attributes, schema, outlined in data/attributes.csv
"""
import glob
import os

import dask.dataframe as dd
import numpy as np
import pandas as pd

import config


class Read:

    def __init__(self):

        self.data_ = config.data_
        self.attributes_ = config.attributes_
        self.path_matrix = config.path_matrix
        self.path_computations = config.path_computations

    def attributes(self) -> (np.ndarray, dict):
        """
        The attributes of the data files to be read

        :return:
        """

        try:
            data = pd.read_csv(filepath_or_buffer=self.attributes_, header=0, usecols=['field', 'type'],
                               dtype={'field': str, 'type': str}, encoding='UTF-8')
        except OSError as err:
            raise err

        fields = data.field.values
        types = data.set_index(keys='field', drop=True).to_dict(orient='dict')['type']
        kwargs = {'usecols': fields, 'encoding': 'UTF-8', 'header': 0, 'dtype': types}

        return kwargs

    def paths(self):

        return glob.glob(pathname=os.path.join(self.data_, '*.csv'))

    def matrices(self, paths: list, kwargs: dict) -> dd.DataFrame:
        """
        Reads-in the files encoded by paths.  Each file is a matrix, together the
        matrices form a single design matrix

        :param paths: The paths to matrix files
        :param kwargs: Parameters for reading the files

        :return:
        """

        try:
            streams = dd.read_csv(urlpath=paths, blocksize=None, **kwargs)
        except OSError as err:
            raise err

        streams.visualize(filename=os.path.join(self.path_computations, 'read'), format='pdf')

        return streams

    def exc(self):
        """
        Returns a design matrix

        :return:
        """

        # The data file paths
        paths = self.paths()

        # The attributes of the files
        kwargs = self.attributes()

        # Hence
        matrices = self.matrices(paths=paths, kwargs=kwargs)
        matrix = matrices.compute(scheduler='processes')
        matrix.to_csv(path_or_buf=os.path.join(self.path_matrix, 'unscaled.csv'), header=True, index=False,
                      encoding='UTF-8')

        return matrix
