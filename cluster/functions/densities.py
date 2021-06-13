import pandas as pd

import numpy as np
import sklearn.metrics


# noinspection PyUnresolvedReferences
class Densities:

    def __init__(self, matrix: np.ndarray, method: str = None):

        self.matrix = matrix
        self.method = method
    
    def points(self, model) -> pd.DataFrame:
        """

        :param model:
        :return:
        """

        # labels
        if self.method == 'sc':
            labels: np.ndarray = model.labels_
        else:
            labels: np.ndarray = model.predict(self.matrix)

        # scores
        scores: np.ndarray = sklearn.metrics.silhouette_samples(
            self.matrix, labels, metric='cosine')
        
        return pd.DataFrame(
            data={'score': scores, 'label': labels}
        )    
    
    def clusters(self, points: pd.DataFrame) -> pd.DataFrame:
        """
                
        :param points:

        :return:
        """    

        aggregates = points.groupby(by='label').agg({'score': [np.median, np.mean, self.density, 'sum', 'count']})
        aggregates = aggregates['score']
        aggregates.reset_index(drop=False, inplace=True)

        return aggregates

    @staticmethod
    def density(series: np.ndarray) -> np.float:

        number_of_rows = series.shape[0]
        quotients = np.true_divide(series, number_of_rows)
        calculation = quotients.sum()

        # condition = (series >= 0)
        # if (np.sum(condition) > 0) & (series[condition].sum() > 0):
        #     quotient = np.true_divide(series[~condition].sum(), series[condition].sum())
        # else:
        #     quotient = 1
        # calculation = 1 - np.absolute(quotient)
                
        return calculation

    def exc(self, model):
        """
        In order to embed 'clusters' in table 'summary' clusters is converted to a 'dict' of 
        orient 'index', which can reconstructed via pd.DataFrame.from_dict(..., orient='index')
        """

        # points: gets the silhouette score of each point
        points = self.points(model=model)

        # clusters: conducts calculations per cluster based on the silhouette scores of the points of a cluster
        clusters = self.clusters(points=points)

        # Hence ...
        values = np.array([[clusters['density'].sum(), clusters.to_dict(orient='index')]])
        columns = ['density', 'clusters']
        
        summary = pd.DataFrame(data=values, columns=columns)

        return summary
