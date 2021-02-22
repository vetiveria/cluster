import collections

import numpy as np


class Parameters:

    def __init__(self):
        self.ParametersCollection = collections.namedtuple(
            typename='ParametersCollection',
            field_names=['array_n_components', 'array_covariance_type', 'array_weight_concentration_prior_type',
                         'metrics', 'random_state'])

    def exc(self):
        return self.ParametersCollection(
            array_n_components=np.arange(3, 9),
            array_covariance_type=np.array(['full', 'diag', 'tied', 'spherical']),
            array_weight_concentration_prior_type=np.array(['dirichlet_process', 'dirichlet_distribution']),
            metrics=['cityblock', 'cosine', 'euclidean', 'l1', 'l2', 'manhattan'],
            random_state=5)
