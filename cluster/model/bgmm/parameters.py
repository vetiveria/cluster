import collections

import numpy as np


class Parameters:

    def __init__(self):
        self.ParametersCollection = collections.namedtuple(
            typename='ParametersCollection',
            field_names=['array_n_components', 'array_covariance_type', 'array_weight_concentration_prior_type',
                         'array_n_init', 'metrics', 'random_state'])

    def exc(self):
        return self.ParametersCollection(
            array_n_components=np.array([3, 5, 6]),
            array_covariance_type=np.array(['full', 'diag', 'tied', 'spherical']),
            array_weight_concentration_prior_type=np.array(['dirichlet_process']),
            array_n_init=np.array([18]),
            metrics=['cityblock', 'cosine', 'euclidean', 'l1', 'l2', 'manhattan'],
            random_state=5)
