import glob
import os

import numpy as np
import pandas as pd

import cluster.src.design
import cluster.src.projections
import config


class Prospects:

    def __init__(self, details: pd.Series, supplements: pd.DataFrame):
        """
        view = ['r_clusters', 'n_clusters', 'scaled_calinski', 'scaled_davies_transform',
            'scaled_density', 'score', 'key_description']

        :param supplements:
        """

        configurations = config.Config()
        self.warehouse = configurations.warehouse

        self.details = details
        self.supplements = supplements

    def directories(self):

        if os.path.exists(self.warehouse):
            files = glob.glob(os.path.join(self.warehouse, '*.csv'))
            [os.remove(file) for file in files]

        if not os.path.exists(self.warehouse):
            os.makedirs(self.warehouse)

    def write(self, original: pd.DataFrame, reduced: pd.DataFrame):

        self.supplements.to_csv(path_or_buf=os.path.join(self.warehouse, 'supplements.csv'), index=False, header=True,
                                encoding='UTF-8')

        original.to_csv(path_or_buf=os.path.join(self.warehouse, 'original.csv'), index=False, header=True,
                        encoding='UTF-8')

        reduced.to_csv(path_or_buf=os.path.join(self.warehouse, 'reduced.csv'), index=False, header=True,
                       encoding='UTF-8')

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

        self.directories()
        self.write(original=original, reduced=reduced)
