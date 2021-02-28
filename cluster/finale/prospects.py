import pandas as pd
import numpy as np

import cluster.src.design
import cluster.src.projections


class Prospects:

    def __init__(self, details: pd.Series, supplements: pd.DataFrame):
        """
        view = ['r_clusters', 'n_clusters', 'scaled_calinski', 'scaled_davies_transform',
            'scaled_density', 'score', 'key_description']

        :param supplements:
        """

        self.details = details
        self.supplements = supplements

    def labels_(self, matrix):

        if self.details.method == 'sc':
            labels: np.ndarray = self.details.model.labels_
        else:
            labels: np.ndarray = self.details.model.predict(matrix)

        return labels

    def exc(self):

        # Projections
        projections = cluster.src.projections.Projections()
        projection = projections.exc(key=self.details.key)

        # The original data set
        design = cluster.src.design.Design().exc()
        original: pd.DataFrame = design.frame
        reduced: pd.DataFrame = projection.frame

        # Adding labels
        labels = self.labels_(matrix=projection.tensor)
        original.loc[:, 'label'] = labels
        reduced.loc[:, 'label'] = labels

        print(original.head().iloc[:, -7:])
        print(reduced.head())
