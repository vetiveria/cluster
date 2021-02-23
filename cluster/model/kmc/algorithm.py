"""
Module algorithm: K Means Clustering
"""

import collections

import dask
import numpy as np
import sklearn.mixture


class Algorithm:

    def __init__(self, matrix: np.ndarray, parameters: collections.namedtuple):

        self.matrix = matrix
        self.parameters = parameters

    def modelling(self, n_clusters):

        try:
            model = sklearn.cluster.KMeans(n_clusters=n_clusters, init='k-means++',
                                           random_state=self.parameters.random_state).fit(X=self.matrix)
        except OSError as _:
            print('Impossible ...K: {}'.format(n_clusters))
            model = None

        return model

    def exc(self):

        computations = [dask.delayed(self.modelling)(n_clusters) for n_clusters in
                        self.parameters.array_n_clusters]

        models = dask.compute(computations, scheduler='processes')[0]
        models = [model for model in models if model is not None]

        return models
