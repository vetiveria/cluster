"""
Module algorithm: Gaussian Mixture Model
"""

import collections

import dask
import numpy as np
import sklearn.mixture


class Algorithm:

    def __init__(self, matrix: np.ndarray, parameters: collections.namedtuple):

        self.matrix = matrix
        self.parameters = parameters

    def modelling(self, n_components, covariance_type):

        try:
            model = sklearn.mixture.GaussianMixture(
                n_components=n_components, covariance_type=covariance_type, tol=0.001, reg_covar=1e-06, max_iter=100,
                n_init=100, init_params='kmeans', weights_init=None, means_init=None, precisions_init=None,
                random_state=self.parameters.random_state, warm_start=False, verbose=0, verbose_interval=10
            ).fit(X=self.matrix)
        except OSError as _:
            print('Impossible ... K: {}, Covariance Type: {}'.format(n_components, covariance_type))
            model = None

        return model

    def exc(self):

        computations = [dask.delayed(self.modelling)(n_components, covariance_type)
                        for n_components in self.parameters.array_n_components
                        for covariance_type in self.parameters.array_covariance_type]

        models = dask.compute(computations, scheduler='processes')[0]
        models = [model for model in models if model is not None]

        return models
