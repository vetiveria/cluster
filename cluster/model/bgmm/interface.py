import logging
import pandas as pd
import config

import cluster.src.projections

import cluster.functions.discriminator

import cluster.model.bgmm.algorithm
import cluster.model.bgmm.determinants
import cluster.model.bgmm.parameters


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

        parameters = cluster.model.bgmm.parameters.Parameters()

        excerpts = []
        for key in self.keys:

            # In focus
            self.logger.info('\n{}\nModelling the {} projections\n'.format(key, self.descriptions[key]))

            # Projection
            projection = self.projections.exc(key=key)

            # The determined models ...
            models: list = cluster.model.bgmm.algorithm.Algorithm(
                matrix=projection.tensor, parameters=parameters).exc()
            determinants: pd.DataFrame = cluster.model.bgmm.determinants.Determinants(
                matrix=projection.tensor, models=models).exc()

            # The best
            best = self.discriminator.exc(determinants=determinants)
            self.logger.info(' The best model\n{}\n'.format(best.estimate))

            excerpts.append(best.properties.iloc[best.index, :])

        inbrief = pd.concat(excerpts, axis=0, ignore_index=True)

        return inbrief
