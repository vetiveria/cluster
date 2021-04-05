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

    def supplements_(self):
        """

        :return:
        """

        self.write(blob=self.supplements, sections=['supplements.csv'])

    def principals_(self):
        """

        :return: The principals w.r.t. a projection in space
        """

        principals: pd.DataFrame = self.projection.frame
        principals.loc[:, 'label'] = self.labels

        self.write(blob=principals, sections=['principals.csv'])

    def releases_(self):
        """

        :return:
        """

        # Original
        design = cluster.src.design.Design().exc()
        original: pd.DataFrame = design.frame
        original.loc[:, 'label'] = self.labels

        melted = original.melt(id_vars=['COUNTYGEOID', 'label'], var_name='tri_chem_id', value_name='quantity_kg')
        assert melted[['COUNTYGEOID', 'label']].drop_duplicates().shape[0] == \
            melted[['COUNTYGEOID']].drop_duplicates().shape[0], "Imbalanced releases data"

        # Releases per determined cluster
        for i in melted['label'].unique():
            frame = melted[melted['label'] == i]
            self.write(blob=frame, sections=['releases', '{:02d}.csv'.format(i)])

        # Reduced releases
        releases = melted[melted['quantity_kg'] > 0].copy()
        self.write(blob=releases, sections=['releases.csv'])

    def write(self, blob: pd.DataFrame, sections: list):
        """

        :param blob: The DataFrame that will be written to disc
        :param sections: The name of the file, including its extension
        :return:
        """

        blob.to_csv(path_or_buf=os.path.join(self.warehouse, *sections), index=False, header=True,
                    encoding='UTF-8')

    def exc(self):
        """
        Weights: All data values are in kilograms, ref.
            https://github.com/vetiveria/spots/blob/master/src/releases/helpers.py#L52

        :return:
        """

        self.principals_()
        self.releases_()
        self.supplements_()
