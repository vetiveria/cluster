"""
Module algorithm: Bayesian Gaussian Mixture Model
"""

import sklearn.mixture
import dask

import numpy as np
import collections


class Algorithm:

    def __init__(self, parameters: collections.namedtuple):

        self.parameters = parameters

    def modelling(self, matrix: np.ndarray, n_components: int, covariance_type: str):

        try:
            model = sklearn.mixture.BayesianGaussianMixture(
                n_components=n_components, covariance_type=covariance_type, tol=0.001, reg_covar=1e-06, max_iter=100,
                n_init=1, init_params='kmeans', weight_concentration_prior_type='dirichlet_process',
                weight_concentration_prior=None, mean_precision_prior=None, mean_prior=None,
                degrees_of_freedom_prior=None, covariance_prior=None, random_state=self.parameters.random_state,
                warm_start=False, verbose=0, verbose_interval=10
            ).fit(X=matrix)
        except OSError as _:
            print('Impossible ... K: {}, Covariance Type: {}'.format(n_components, covariance_type))
            model = None

        return model

    def exc(self, matrix: np.ndarray):
        
        models = [dask.delayed(self.modelling)(matrix, n_components, covariance_type) 
                  for n_components in self.parameters.array_n_components
                  for covariance_type in self.parameters.array_covariance_type]

        return models
