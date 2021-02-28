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
            array_n_clusters=np.array([6]),
            array_eigen_solver=np.array(['arpack', 'lobpcg']),
            array_n_init=np.array([15]),
            array_gamma=np.array([1.0, 1.1, 1.2, 1.3]),
            array_affinity=np.array(['laplacian']),
            array_n_neighbours=np.arange(10, 11),
            random_state=5)
