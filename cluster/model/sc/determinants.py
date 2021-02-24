import dask
import numpy as np
import pandas as pd
import sklearn.cluster

import cluster.functions.densities
import cluster.functions.measures


class Determinants:

    def __init__(self, matrix: np.ndarray, models: list):
        """

        :param matrix:
        :param models:
        """

        self.models = models
        self.matrix = matrix

        self.densities = cluster.functions.densities.Densities(matrix=matrix)
        self.measures = cluster.functions.measures.Measures(matrix=matrix)

    @dask.delayed
    def properties_(self, model: sklearn.cluster.SpectralClustering):
        """
        Re-name n_components -> clusters_requested; this will avoid the confusion with # of principal components

        :param model:
        :return:
        """

        values = np.array([model.n_clusters, np.unique(model.fit_predict(self.matrix)).shape[0], model])

        columns = ['n_components', 'n_clusters', 'model']

        return pd.DataFrame(data=values, columns=columns)

    @dask.delayed
    def densities_(self, model: sklearn.cluster.SpectralClustering):
        """

        :param model:
        :return:
        """

        return self.densities.exc(model=model)

    @dask.delayed
    def measures_(self, model: sklearn.cluster.SpectralClustering):
        """

        :param model:
        :return:
        """

        return self.measures.exc(model=model)

    @dask.delayed
    def concatenate(self, measures, densities, properties):
        """

        :param measures:
        :param densities:
        :param properties:
        :return:
        """

        return pd.concat([measures, densities, properties], axis=1)

    def exc(self):
        """

        :return:
        """

        calculations = []

        for model in self.models:
            measures = self.measures_(model=model)
            densities = self.densities_(model=model)
            properties = self.properties_(model=model)

            calculations.append(self.concatenate(measures, densities, properties))

        dask.visualize(calculations, filename='calculations', format='pdf')
        values = dask.compute(calculations, scheduler='processes')[0]
        return pd.concat(values, ignore_index=True)
