import collections
import numpy as np
import pandas as pd

import sklearn.metrics

class Measures:

    def __init__(self, matrix: np.ndarray):
        """
        The constructor
        
        """

        self.matrix = matrix    

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
        

    def silhouette(self, scores):
        """
        Calculates the silhouette medians \\uparrow & silhouette mean \\uparrow.  Note: the silhouette mean determined
        via 
            mean(the scores calculated by sklearn.metrics.silhouette_samples)
        is equivalent to 
            sklearn.metrics.silhouette_score

        """
        
        Silhouette = collections.namedtuple(typename='Silhouette', field_names=['mean', 'median'])
        
        return Silhouette(mean = scores.mean(), median = np.median(scores))
        

    def exc(self, model):
        """
        A summary of scores and characteristics
        
        """

        # Baseline
        labels: np.ndarray = model.predict(self.matrix)
        scores: np.ndarray = sklearn.metrics.silhouette_samples(
            self.matrix, model.predict(self.matrix), metric='cosine')

        # Silhouette
        silhouette = self.silhouette(scores=scores)
        
        # In summary
        values = np.array([[self.calinski(labels=labels), self.davies(labels=labels), silhouette.median, silhouette.mean]])
        
        columns = ['calinski', 'davies', 'silhouette_median', 'sihouette_mean']

        summary = pd.DataFrame(values, columns=columns)
        summary.loc[:, 'davies_transform'] = np.exp(-summary['davies'])

        return summary







