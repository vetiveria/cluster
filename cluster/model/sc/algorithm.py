"""
Module algorithm: Spectral Clustering Model
"""

import collections

import dask
import numpy as np
import sklearn.cluster


class Algorithm:

    def __init__(self, matrix: np.ndarray, parameters: collections.namedtuple):
        """
        
        :param matrix:
        :param parameters:
        """

        self.matrix = matrix
        self.parameters = parameters

    def modelling(self, n_clusters, eigen_solver, n_init, gamma, affinity, n_neighbours):
        """

        :param n_clusters:
        :param eigen_solver:
        :param n_init:
        :param gamma:
        :param affinity:
        :param n_neighbours:
        :return:
        """

        try:
            model = sklearn.cluster.SpectralClustering(n_clusters=n_clusters, eigen_solver=eigen_solver,
                                                       n_components=None,
                                                       random_state=self.parameters.random_state, n_init=n_init,
                                                       gamma=gamma, affinity=affinity, n_neighbors=n_neighbours,
                                                       eigen_tol=0.0, assign_labels='discretize', degree=3, coef0=1,
                                                       kernel_params=None, n_jobs=None).fit(X=self.matrix)
        except OSError as _:
            print('Impossible ... requested clusters: {}, eigenvalue solver: {}'.format(n_clusters, eigen_solver))
            model = None

        return model

    def exc(self):
        """

        :return:
        """

        computations = [
            dask.delayed(self.modelling)(n_clusters, eigen_solver, n_init, gamma, affinity, n_neighbours)
            for n_clusters in self.parameters.array_n_clusters
            for eigen_solver in self.parameters.array_eigen_solver
            for n_init in self.parameters.array_n_init
            for gamma in self.parameters.array_gamma
            for affinity in self.parameters.array_affinity
            for n_neighbours in self.parameters.array_n_neighbours]

        models = dask.compute(computations, scheduler='processes')[0]
        models = [model for model in models if model is not None]

        return models
