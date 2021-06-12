import collections
import logging
import pandas as pd
import os
import config

import cluster.src.projections

import cluster.functions.discriminator

import cluster.model.sc.algorithm
import cluster.model.sc.determinants
import cluster.model.sc.parameters


class Interface:

    def __init__(self, group: str, kernels: dict):
        """
        Constructor
        :param group:
        :param kernels: The metadata details of the kernel projections that would undergo clustering
        """

        self.method = 'sc'
        self.group = group
        self.kernels = kernels

        # Configurations
        configurations = config.Config()
        self.directory = os.path.join(configurations.warehouse, self.group)

        # And, the data projections that will be modelled
        self.projections = cluster.src.projections.Projections()
        self.discriminator = cluster.functions.discriminator.Discriminator()
        self.parameters = cluster.model.sc.parameters.Parameters().exc()

        # Method store within a group directory
        self.store = os.path.join(self.directory, self.method)
        if not os.path.exists(self.store):
            os.makedirs(self.store)

    @staticmethod
    def datum_():
        """

        :return:
        """

        return collections.namedtuple(typename='Datum',
                                      field_names=['group', 'key', 'url', 'description', 'identifiers'])

    def exc(self):
        """

        :return:
        """

        excerpts = []
        for key_, arg in self.kernels.items():

            datum = self.datum_()._make((self.group, key_, arg['url'], arg['description'], arg['identifiers']))

            # In focus
            logging.info('Spectral Clustering: Modelling the {} projections'.format(datum.description))

            # Projection
            projection = self.projections.exc(datum=datum)

            # The determined models ...
            models: list = cluster.model.sc.algorithm.Algorithm(
                matrix=projection.tensor, parameters=self.parameters).exc()
            determinants = cluster.model.sc.determinants.Determinants(
                matrix=projection.tensor, models=models, method=self.method).exc()

            # The best
            best = self.discriminator.exc(determinants=determinants)
            best.properties.to_csv(path_or_buf=os.path.join(self.store, datum.key + '.csv'),
                                   index=False, header=True, encoding='utf-8')

            # ... the best w.r.t. a kernel/datum.key type
            vector = best.properties.copy().iloc[best.index:(best.index + 1), :]
            vector.loc[:, 'key'] = datum.key
            vector.loc[:, 'key_description'] = datum.description
            vector.loc[:, 'method'] = self.method

            # Append
            excerpts.append(vector)

        # Concatenate ... this will have a model per kernel/key type
        excerpt = pd.concat(excerpts, axis=0, ignore_index=True)
        excerpt.to_csv(path_or_buf=os.path.join(self.directory, self.method + '.csv'),
                       index=False, header=True, encoding='utf-8')

        # Common steps ... this set of steps selects the best model from the best per kernel/key type
        index = excerpt['score'].idxmax()
        summary = excerpt.iloc[index:(index + 1), :]
        summary.reset_index(drop=True, inplace=True)

        return summary
