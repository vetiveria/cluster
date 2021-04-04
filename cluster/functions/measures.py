import collections
import numpy as np
import pandas as pd

import sklearn.metrics


# noinspection PyUnresolvedReferences,PyProtectedMember
class Measures:

    def __init__(self, matrix: np.ndarray, method: str = None):
        """
        The constructor
        
        """

        self.matrix = matrix
        self.method = method

    def calinski(self, labels: np.ndarray):
        """
        Calinski \\uparrow

        """

        return sklearn.metrics.calinski_harabasz_score(self.matrix, labels)

    def davies(self, labels: np.ndarray):
        """
        Davies \\downarrow

        """

        return sklearn.metrics.davies_bouldin_score(self.matrix, labels)

    @staticmethod
    def silhouette(scores):
        """
        Calculates the silhouette medians \\uparrow & silhouette mean \\uparrow.  Note: the silhouette mean determined
        via 
            mean(the scores calculated by sklearn.metrics.silhouette_samples)
        is equivalent to 
            sklearn.metrics.silhouette_score

        """
        
        Silhouette = collections.namedtuple(typename='Silhouette', field_names=['mean', 'median'])
        
        return Silhouette._make((scores.mean(), np.median(scores)))

    def exc(self, model):
        """
        A summary of scores and characteristics
        
        """

        # Baseline
        if self.method == 'sc':
            labels: np.ndarray = model.labels_
        else:
            labels: np.ndarray = model.predict(self.matrix)

        scores: np.ndarray = sklearn.metrics.silhouette_samples(
            self.matrix, labels, metric='cosine')

        # Silhouette
        silhouette = self.silhouette(scores=scores)
        
        # In summary
        values = np.array([[self.calinski(labels=labels), self.davies(labels=labels),
                            silhouette.median, silhouette.mean]])
        
        columns = ['calinski', 'davies', 'silhouette_median', 'silhouette_mean']

        summary = pd.DataFrame(values, columns=columns)
        summary.loc[:, 'calinski_inverse'] = np.true_divide(1, summary['calinski'])

        return summary
