import pandas as pd

import numpy as np
import sklearn.metrics


class Densities:

    def __init__(self, matrix: np.ndarray):

        self.matrix = matrix        
    
    def points(self, model) -> pd.DataFrame:

        labels: np.ndarray = model.predict(self.matrix)
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
    def density(series) -> np.float:

        condition = (series >= 0)

        if (np.sum(condition) > 0) & (series[condition].sum() > 0):
            quotient = np.true_divide(series[~condition].sum(), series[condition].sum())
        else:
            quotient = 1
                
        return 1 - np.absolute(quotient)

    def exc(self, model):
        """
        In order to embed 'clusters' in table 'summary' clusters is converted to a 'dict' of 
        orient 'index', which can reconstructed via pd.DataFrame.from_dict(..., orient='index')
        """

        # points
        points = self.points(model=model)

        # clusters        
        clusters = self.clusters(points=points)

        # Hence
        values = np.array([[clusters['density'].sum(), clusters.to_dict(orient='index')]])
        columns = ['density', 'clusters']
        
        summary = pd.DataFrame(data=values, columns=columns)

        return summary
