import logging
import pandas as pd
import config

import cluster.src.projections

import cluster.functions.discriminator

import cluster.model.kmc.parameters
import cluster.model.kmc.algorithm
import cluster.model.kmc.determinants


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

        parameters = cluster.model.kmc.parameters.Parameters().exc()

        excerpts = []
        properties = []
        for key in self.keys:

            # In focus
            self.logger.info('K Means: Modelling the {} projections\n'.format(self.descriptions[key]))

            # Projection
            projection = self.projections.exc(key=key)

            # The determined models ...
            models: list = cluster.model.kmc.algorithm.Algorithm(
                matrix=projection.tensor, parameters=parameters).exc()
            determinants: pd.DataFrame = cluster.model.kmc.determinants.Determinants(
                matrix=projection.tensor, models=models).exc()

            # The best
            best = self.discriminator.exc(determinants=determinants)

            vector = best.properties.copy().iloc[best.index:(best.index + 1), :]
            vector.loc[:, 'key'] = key
            vector.loc[:, 'key_description'] = self.descriptions[key]

            # Append
            excerpts.append(vector)
            properties.append(best.properties)

        # Concatenate
        excerpt = pd.concat(excerpts, axis=0, ignore_index=True)

        # Common steps
        index = excerpt['score'].idxmax()
        summary = excerpt.iloc[index:(index + 1), :]
        summary.reset_index(drop=True, inplace=True)

        return summary, properties[index]
