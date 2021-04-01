import collections

import numpy as np


class Parameters:

    def __init__(self):

        self.ParametersCollection = collections.namedtuple(typename='ParametersCollection',
                                                           field_names=['array_n_clusters', 'random_state'])

    def exc(self):
        
        return self.ParametersCollection(array_n_clusters=np.array([5, 6]), random_state=5)
