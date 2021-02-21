import numpy as np
import pandas as pd
import sklearn.metrics

import config


class Measures:

    def __init__(self, principals):
        self.distance_metric = config.distance_metric

        self.principals = principals
        self.matrix = self.principals.drop(columns=config.identifier).values

    def details(self, labels: np.ndarray):
        data = self.principals.copy()
        data['label'] = labels
        data['score'] = sklearn.metrics.silhouette_samples(self.matrix, labels, metric=self.distance_metric)

        return data

    def calinski(self, labels: np.ndarray):
        return ['calinski', sklearn.metrics.calinski_harabasz_score(self.matrix, labels)]

    def davies(self, labels: np.ndarray):
        return ['davies', sklearn.metrics.davies_bouldin_score(self.matrix, labels)]

    @staticmethod
    def ethereal(data):
        median = ['silhouette median', data.score.median()]
        mean = ['silhouette mean', data.score.mean()]

        return median, mean

    @staticmethod
    def silhouettes(data: pd.DataFrame):
        values = data[['label', 'score']].groupby(by='label').median()
        values.reset_index(drop=False, inplace=True)
        values['measure'] = 'silhouette median of cluster'

        return values

    @staticmethod
    def outline(measurements: pd.DataFrame, model: str, matrix_type: str, nclusters: int,
                marginal: str, covariance: str):
        measurements['model'] = model
        measurements['matrix'] = matrix_type
        measurements['K'] = nclusters
        measurements['covariance'] = covariance
        measurements['marginal'] = marginal

        return measurements

    def exc(self, labels: np.ndarray, matrix_type: str, model: str, marginal: str, covariance: str = None):
        data = self.details(labels=labels)
        nclusters = data.label.unique().shape[0]

        calinski = self.calinski(labels)
        davies = self.davies(labels)
        median, mean = self.ethereal(data=data)
        measurements = pd.DataFrame(np.array([calinski, davies, median, mean]), columns=['measure', 'score'])
        measurements['label'] = None

        silhouettes = self.silhouettes(data=data)
        measurements = pd.concat((measurements, silhouettes), ignore_index=True, axis=0)

        return self.outline(measurements=measurements, model=model, matrix_type=matrix_type, nclusters=nclusters,
                            marginal=marginal, covariance=covariance)
