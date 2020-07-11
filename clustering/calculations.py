import glob
import os

import dask
import dask.dataframe
import pandas as pd

import clustering.matrix.read
import clustering.projections.interface
import config


class Calculations:

    def __init__(self):

        self.path_matrix = config.path_matrix
        self.projection_methods = list(config.algorithms.keys())

        read = clustering.matrix.read.Read()
        self.kwargs = read.attributes()

    @staticmethod
    def filestrings():

        return glob.glob(os.path.join(config.path_matrix, '*.csv'))

    def read(self, filestring: str):

        try:
            matrix = pd.read_csv(filepath_or_buffer=filestring, header=0,
                                 encoding='UTF-8', dtype=self.kwargs['dtype'])
        except OSError as err:
            raise err

        return matrix

    def dimension_reduction(self, filestring, projection_method):

        # Get a design matrix
        matrix = self.read(filestring=filestring)

        # Matrix type
        matrix_type = os.path.splitext(os.path.basename(filestring))[0]

        # Apply a dimensionality reduction method
        projections = clustering.projections.interface.Interface()
        message = projections.exc(matrix=matrix, matrix_type=matrix_type, projection_method=projection_method)
        print(message)

    def exc(self):

        # The ...
        filestrings = self.filestrings()

        combinations = [{'filestring': filestring, 'projection_method': projection_method}
                        for filestring in filestrings for projection_method in self.projection_methods]

        # Hence
        computations = [
            dask.delayed(self.dimension_reduction)(combination['filestring'], combination['projection_method'])
            for combination in combinations]
        dask.visualize(computations, filename='calculations', format='pdf')
        dask.compute(computations, scheduler='processes')
