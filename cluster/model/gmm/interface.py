import logging
import pandas as pd
import config

import cluster.src.projections

import cluster.functions.discriminator

import cluster.model.gmm.algorithm
import cluster.model.gmm.determinants
import cluster.model.gmm.parameters


class Interface:

    def __init__(self):

        # Configurations
        configurations = config.Config()

        # The keys of the projection matrices, and their descriptions
        self.keys = configurations.keys
        self.descriptions = configurations.descriptions_()

        # And, the data projections that will be modelled
        self.projections = cluster.src.projections.Projections()
        self.discriminator = cluster.functions.discriminator.Discriminator()

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='%(message)s%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)

    def exc(self):

        parameters = cluster.model.gmm.parameters.Parameters().exc()

        excerpts = []
        for key in self.keys:

            if key != 'cosine':
                continue

            # In focus
            self.logger.info('Gaussian Mixture Model: Modelling the {} projections\n'.format(self.descriptions[key]))

            # Projection
            projection = self.projections.exc(key=key)

            # The determined models ...
            models: list = cluster.model.gmm.algorithm.Algorithm(
                matrix=projection.tensor, parameters=parameters).exc()
            determinants: pd.DataFrame = cluster.model.gmm.determinants.Determinants(
                matrix=projection.tensor, models=models).exc()

            # The best
            best = self.discriminator.exc(determinants=determinants)

            vector = best.properties.copy().iloc[best.index:(best.index + 1), :]
            vector.loc[:, 'key'] = key
            vector.loc[:, 'key_description'] = self.descriptions[key]

            # Append
            excerpts.append(vector)

        # Concatenate
        summary = pd.concat(excerpts, axis=0, ignore_index=True)

        return summary
