import dask
import numpy as np
import pandas as pd
import sklearn.cluster

import clustering.functions.margin
import clustering.clusters.measures
import config


class KMC:

    def __init__(self, principals, matrix_type):

        self.name = 'k means clustering'
        self.marginal = 'inertia'

        self.random_state = config.random_state
        self.array_of_k = config.array_of_k

        self.principals = principals
        self.matrix = self.principals.drop(columns=config.identifier).values
        self.matrix_type = matrix_type

    def modelling(self, n_clusters):

        try:
            model = sklearn.cluster.KMeans(n_clusters=n_clusters, init='k-means++',
                                           random_state=self.random_state).fit(X=self.matrix)
        except Exception as err:
            print(err)
            print('K Means Clustering -> Skipping K: {}'.format(n_clusters))
            model = None

        return model

    @staticmethod
    def inertia(models):

        margin = clustering.functions.margin.Margin()

        # Get the inertia values
        inertia_ = [[i.inertia_, i.n_clusters] for i in models]
        inertia = pd.DataFrame(data=inertia_, columns=['inertia', 'K'])

        # For sequential analysis, ensure that the table's data is sorted by K
        inertia.sort_values(by=['K'], inplace=True)
        index, properties, field = margin.exc(values=inertia.inertia)
        inertia = inertia[['K']].join(properties)

        return index, inertia, field

    @staticmethod
    def best(models, selection):

        estimate = [model for model in models if (model.n_clusters == selection.K)]
        return estimate[0]

    def measurements(self, estimate: sklearn.cluster.KMeans):

        measures = clustering.clusters.measures.Measures(self.principals)
        return measures.exc(labels=estimate.labels_, matrix_type=self.matrix_type, model=self.name,
                            marginal=self.marginal)

    def exc(self):

        computations = [dask.delayed(self.modelling)(n_clusters) for n_clusters in self.array_of_k]
        models = dask.compute(computations, scheduler='processes')[0]
        models = [model for model in models if model is not None]

        index, inertia, field = self.inertia(models=models)
        if np.isnan(index):
            estimate = None
            measurements = None
        else:
            estimate = self.best(models=models, selection=inertia.loc[index])
            measurements = self.measurements(estimate=estimate)

        return estimate, measurements
