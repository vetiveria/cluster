import logging
import pandas as pd
import config

import cluster.src.design

import cluster.functions.discriminator

import cluster.model.sc.algorithm
import cluster.model.sc.determinants
import cluster.model.sc.parameters


class Interface:

    def __init__(self):
        """

        """

        # Configurations
        configurations = config.Config()

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='%(message)s%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def determinants() -> pd.DataFrame:

        # The modelling parameters
        parameters = cluster.model.sc.parameters.Parameters().exc()

        # The design matrix; the spectral clustering model determines the appropriate number of decomposition
        # principal components w.r.t. a requested number of clusters
        design = cluster.src.design.Design().exc()

        # The determined models ...
        models: list = cluster.model.sc.algorithm.Algorithm(matrix=design, parameters=parameters).exc()

        return cluster.model.sc.determinants.Determinants(matrix=design, models=models).exc()

    def exc(self):
        """

        :return:
        """

        # In focus
        self.logger.info('Spectral Clustering\n')

        # Modelling & Performance Determinants
        determinants = self.determinants()

        # The best
        best = cluster.functions.discriminator.Discriminator().exc(determinants=determinants)

        vector: pd.DataFrame = best.properties.copy().iloc[best.index:(best.index + 1), :]
        vector.loc[:, 'key'] = best.estimate.eigen_solver
        vector.loc[:, 'key_description'] = 'A spectral clustering model eigenvalue decomposition method'

        summary = vector.reset_index(drop=True)

        return summary
