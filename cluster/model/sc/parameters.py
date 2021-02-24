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
            array_n_clusters=np.arange(3, 9),
            array_eigen_solver=np.array(['arpack', 'lobpcg']),
            array_n_init=np.array([11, 13]),
            array_gamma=np.arange(start=0.4, stop=1.8, step=0.2),
            array_affinity=np.array(['polynomial', 'rbf', 'laplacian', 'sigmoid', 'cosine']),
            array_n_neighbours=np.arange(10, 13),
            random_state=5)
