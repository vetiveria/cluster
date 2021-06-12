import logging
import pandas as pd
import os
import config

import cluster.src.projections

import cluster.functions.discriminator

import cluster.model.kmc.parameters
import cluster.model.kmc.algorithm
import cluster.model.kmc.determinants


class Interface:

    def __init__(self, group: str, kernels: dict):
        """
        Constructor
        :param group:
        :param kernels: The metadata details of the kernel projections that would undergo clustering
        """

        self.method = 'kmc'
        self.group = group
        self.kernels = kernels

        # Configurations
        configurations = config.Config()
        self.directory = os.path.join(configurations.warehouse, self.group)

        # And, the data projections that will be modelled
        self.projections = cluster.src.projections.Projections()
        self.discriminator = cluster.functions.discriminator.Discriminator()

        # Logging
        logging.basicConfig(level=logging.INFO, format='%(message)s%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)

    def exc(self):

        store = os.path.join(self.directory, self.method)
        if not os.path.exists(store):
            os.makedirs(store)

        parameters = cluster.model.kmc.parameters.Parameters().exc()
        excerpts = []
        for key_, arg in self.kernels.items():

            # In focus
            self.logger.info('K Means: Modelling the {} projections'.format(arg['description']))

            # Projection
            projection = self.projections.exc(group=self.group, key=key_)

            # The determined models ...
            models: list = cluster.model.kmc.algorithm.Algorithm(
                matrix=projection.tensor, parameters=parameters).exc()
            determinants: pd.DataFrame = cluster.model.kmc.determinants.Determinants(
                matrix=projection.tensor, models=models).exc()

            # The best
            best = self.discriminator.exc(determinants=determinants)
            best.properties.to_csv(path_or_buf=os.path.join(store, key_ + '.csv'),
                                   index=False, header=True, encoding='utf-8')

            # ... the best w.r.t. a kernel/key_ type
            vector = best.properties.copy().iloc[best.index:(best.index + 1), :]
            vector.loc[:, 'key'] = key_
            vector.loc[:, 'key_description'] = arg['description']
            vector.loc[:, 'method'] = self.method

            # Append
            excerpts.append(vector)

        # Concatenate ... this will have a model per kernel/key_ type
        excerpt = pd.concat(excerpts, axis=0, ignore_index=True)
        excerpt.to_csv(path_or_buf=os.path.join(self.directory, self.method + '.csv'),
                       index=False, header=True, encoding='utf-8')

        # Common steps ... this set of steps selects the best model from the best per kernel/key_ type
        index = excerpt['score'].idxmax()
        summary = excerpt.iloc[index:(index + 1), :]
        summary.reset_index(drop=True, inplace=True)

        return summary
