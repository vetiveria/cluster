import dask
import numpy as np
import pandas as pd

import sklearn.mixture

import cluster.functions.densities
import cluster.functions.measures


class Determinants:

    def __init__(self, models: list, matrix: np.ndarray):
        """

        :param models:
        :param matrix: The projection array in focus
        """

        self.models = models
        self.matrix = matrix

        self.densities = cluster.functions.densities.Densities(matrix=matrix)
        self.measures = cluster.functions.measures.Measures(matrix=matrix)

    @dask.delayed
    def properties_(self, model: sklearn.mixture.GaussianMixture):
        """

        :param model:

        :return:
        """

        values = np.array([[model.n_components, np.unique(model.predict(self.matrix)).shape[0],
                            model.bic(self.matrix), model.covariance_type, model]])

        columns = ['n_components', 'n_clusters', 'bic', 'covariance_type', 'model']

        return pd.DataFrame(data=values, columns=columns)

    @dask.delayed
    def densities_(self, model: sklearn.mixture.GaussianMixture):
        """

        :param model:
        :return:
        """

        return self.densities.exc(model=model)

    @dask.delayed
    def measures_(self, model: sklearn.mixture.GaussianMixture):
        """

        :return:
        """

        return self.measures.exc(model=model)

    @dask.delayed
    def concatenate(self, measures, densities, properties):

        return pd.concat([measures, densities, properties], axis=1)

    def exc(self):
        calculations = []

        for model in self.models:
            measures = self.measures_(model=model)
            densities = self.densities_(model=model)
            properties = self.properties_(model=model)

            calculations.append(self.concatenate(measures, densities, properties))

        dask.visualize(calculations, filename='calculations', format='pdf')
        values = dask.compute(calculations, scheduler='processes')[0]

        return pd.concat(values, ignore_index=True)
