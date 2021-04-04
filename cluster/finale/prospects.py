import logging
import os

import numpy as np
import pandas as pd

import cluster.src.design
import cluster.src.projections
import config


class Prospects:

    def __init__(self, details: pd.Series, supplements: pd.DataFrame):
        """

        :param details:
        :param supplements:
        """

        # Configurations
        configurations = config.Config()
        self.warehouse = configurations.warehouse

        # Logging
        logging.basicConfig(level=logging.INFO, format='%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)

        # Calculations
        self.details = details
        self.supplements = supplements

        # Design & Projections Matrices
        self.design = cluster.src.design.Design().exc()

        self.projections = cluster.src.projections.Projections()
        self.projection = self.projections.exc(key=self.details.key)
        self.labels = self.labels_(matrix=self.projection.tensor)

    def labels_(self, matrix):
        """

        :param matrix: The labels of this matrix will be extracted/determined
        :return:
        """

        if self.details.method == 'sc':
            labels: np.ndarray = self.details.model.labels_
        else:
            labels: np.ndarray = self.details.model.predict(matrix)

        return labels

    def data_(self) -> (pd.DataFrame, pd.DataFrame):
        """

        :return: The original data set, and its principals w.r.t. a projection in space
        """

        # Principals
        principals: pd.DataFrame = self.projection.frame
        principals.loc[:, 'label'] = self.labels

        # Original
        original: pd.DataFrame = self.design.frame
        original.loc[:, 'label'] = self.labels

        return principals, original

    def write(self, blob: pd.DataFrame, name: str):
        """

        :param blob: The DataFrame that will be written to disc
        :param name: The name of the file, including its extension
        :return:
        """

        blob.to_csv(path_or_buf=os.path.join(self.warehouse, name), index=False, header=True,
                    encoding='UTF-8')

    def exc(self):
        """
        Weights: All data value are in kilograms, ref.
            https://github.com/vetiveria/spots/blob/master/src/releases/helpers.py#L52

        :return:
        """

        principals, original = self.data_()

        melted = original.melt(id_vars=['COUNTYGEOID', 'label'], var_name='tri_chem_id', value_name='quantity_kg')
        print('\n')
        self.logger.info(melted.info())
        self.logger.info('\n# of distinct county & label pairs: {}'.format(
            melted[['COUNTYGEOID', 'label']].drop_duplicates().shape))
        self.logger.info('\n# of distinct counties: {}'.format(
            melted[['COUNTYGEOID']].drop_duplicates().shape))

        releases = melted[melted['quantity_kg'] > 0].copy()
        print('\n')
        self.logger.info(releases.info())

        self.write(blob=releases, name='releases.csv')
        self.write(blob=principals, name='principals.csv')
        self.write(blob=self.supplements, name='supplements.csv')
