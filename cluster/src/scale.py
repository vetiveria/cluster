import pandas as pd
import sklearn.preprocessing
import os
import dask

import config


class Scale:

    def __init__(self):
        self.exclude = config.exclude
        self.path_matrix = config.path_matrix
        self.path_computations = config.path_computations
        self.scalers = config.scalers

    @staticmethod
    def standard(matrix: pd.DataFrame):
        return sklearn.preprocessing.StandardScaler().fit_transform(X=matrix)

    @staticmethod
    def robust(matrix: pd.DataFrame):
        return sklearn.preprocessing.RobustScaler().fit_transform(X=matrix)

    def scaling(self, data, method):

        values = data.drop(columns=self.exclude)

        matrix = {
            'robust': self.robust(matrix=values),
            'standard': self.standard(matrix=values)
        }.get(method, LookupError('Unknown scaling method - {}'.format(method)))

        scaled = pd.DataFrame(data=matrix, columns=data.columns.drop(labels=self.exclude))
        scaled = data[self.exclude].join(scaled)
        scaled.to_csv(path_or_buf=os.path.join(self.path_matrix, '{}.csv'.format(method)),
                      header=True, index=False, encoding='UTF-8')

    def exc(self, data: pd.DataFrame):

        computations = [dask.delayed(self.scaling)(data, method) for method in self.scalers]
        dask.visualize(computations, filename=os.path.join(self.path_computations, 'scale'), format='pdf')
        dask.compute(computations, scheduler='processes')
