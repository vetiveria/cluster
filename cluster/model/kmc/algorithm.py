"""
Module algorithm: K Means Clustering
"""

import collections

import dask
import numpy as np
import sklearn.mixture


class Algorithm:

    def __init__(self, parameters: collections.namedtuple):

        self.parameters = parameters

    def modelling(self, matrix, n_clusters):

        try:
            model = sklearn.cluster.KMeans(n_clusters=n_clusters, init='k-means++',
                                           random_state=self.parameters.random_state).fit(X=matrix)
        except OSError as _:
            print('Impossible ...K: {}'.format(n_clusters))
            model = None

        return model

    def exc(self, matrix: np.ndarray):

        computations = [dask.delayed(self.modelling)(matrix, n_clusters) for n_clusters in
                        self.parameters.array_n_clusters]

        models = dask.compute(computations, scheduler='processes')[0]
        models = [model for model in models if model is not None]

        return models
