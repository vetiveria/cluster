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

        self.projections = cluster.src.projections.Projections()
        self.projection = self.projections.exc(key=self.details.key)
        self.labels = self.labels_(matrix=self.projection.tensor)

        self.design = cluster.src.design.Design().exc()

    def labels_(self, matrix):

        if self.details.method == 'sc':
            labels: np.ndarray = self.details.model.labels_
        else:
            labels: np.ndarray = self.details.model.predict(matrix)

        return labels

    def data_(self) -> (pd.DataFrame, pd.DataFrame):

        # Principals
        principals: pd.DataFrame = self.projection.frame
        principals.loc[:, 'label'] = self.labels

        # Original
        original: pd.DataFrame = self.design.frame
        original.loc[:, 'label'] = self.labels

        return principals, original

    def write(self, blob: pd.DataFrame, name: str):

        blob.to_csv(path_or_buf=os.path.join(self.warehouse, name), index=False, header=True,
                    encoding='UTF-8')

    def exc(self):
        # Weights:
        # https://github.com/vetiveria/spots/blob/master/src/releases/helpers.py#L52

        principals, original = self.data_()

        melted = original.melt(id_vars=['COUNTYGEOID', 'label'], var_name='tri_chem_id', value_name='quantity_kg')
        print(melted.head())
        print(melted.info())
        print(melted[['COUNTYGEOID', 'label']].drop_duplicates().shape)
        print(melted[['COUNTYGEOID']].drop_duplicates().shape)

        self.write(blob=principals, name='principals.csv')
        self.write(blob=self.supplements, name='supplements.csv')
