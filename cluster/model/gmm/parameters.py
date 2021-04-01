import collections

import numpy as np


class Parameters:

    def __init__(self):
        self.ParametersCollection = collections.namedtuple(typename='ParametersCollection',
                                                           field_names=['array_n_components', 'array_covariance_type',
                                                                        'metrics', 'random_state'])

    def exc(self):
        return self.ParametersCollection(
            array_n_components=np.array([5, 6]),
            array_covariance_type=np.array(['full', 'diag', 'tied', 'spherical']),
            metrics=['cityblock', 'cosine', 'euclidean', 'l1', 'l2', 'manhattan'],
            random_state=5)
