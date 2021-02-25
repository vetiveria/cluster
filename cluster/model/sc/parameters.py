import collections

import numpy as np


class Parameters:

    def __init__(self):
        self.ParametersCollection = collections.namedtuple(
            typename='ParametersCollection',
            field_names=['array_n_clusters', 'array_eigen_solver', 'array_n_init',
                         'array_gamma', 'array_affinity', 'array_n_neighbours', 'random_state'])

    def exc(self):
        return self.ParametersCollection(
            array_n_clusters=np.arange(4, 7),
            array_eigen_solver=np.array(['lobpcg']),
            array_n_init=np.arange(start=9, stop=10, step=1),
            array_gamma=np.arange(start=0.8, stop=1.2, step=0.1),
            array_affinity=np.array(['nearest_neighbors', 'rbf', 'laplacian']),
            array_n_neighbours=np.arange(10, 12),
            random_state=5)
