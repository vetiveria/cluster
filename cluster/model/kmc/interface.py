import collections
import logging
import pandas as pd
import os

import cluster.src.projections

import cluster.functions.discriminator

import cluster.model.kmc.parameters
import cluster.model.kmc.algorithm
import cluster.model.kmc.determinants


class Interface:

    def __init__(self, group: str, kernels: dict, directory: str):
        """
        Constructor
        :param group: baseline?, cancer?, kidney?
        :param kernels: The metadata details of the kernel projections that would undergo clustering
        :param directory: The directory for the group's calculations
        """

        self.method = 'kmc'
        self.group = group
        self.kernels = kernels

        # Configurations
        self.directory = directory

        # And, the data projections that will be modelled
        self.projections = cluster.src.projections.Projections()
        self.discriminator = cluster.functions.discriminator.Discriminator()
        self.parameters = cluster.model.kmc.parameters.Parameters().exc()

        # Method store within a group directory
        self.store = os.path.join(self.directory, self.method)

    @staticmethod
    def datum_():
        """

        :return:
        """

        return collections.namedtuple(typename='Datum',
                                      field_names=['group', 'method', 'key', 'url', 'description', 'identifiers'])

    def exc(self):
        """

        :return:
        """

        if not os.path.exists(self.store):
            os.makedirs(self.store)

        excerpts = []
        for key_, arg in self.kernels.items():

            datum = self.datum_()._make((self.group, self.method, key_, arg['url'], arg['description'], arg['identifiers']))

            # In focus
            logging.info('K Means: Modelling the {} projections'.format(datum.description))

            # Projection
            projection = self.projections.exc(datum=datum)

            # The determined models ...
            models: list = cluster.model.kmc.algorithm.Algorithm(
                matrix=projection.tensor, parameters=self.parameters).exc()
            determinants: pd.DataFrame = cluster.model.kmc.determinants.Determinants(
                matrix=projection.tensor, models=models).exc()

            # The best
            best = self.discriminator.exc(determinants=determinants)
            best.properties.to_csv(path_or_buf=os.path.join(self.store, datum.key + '.csv'),
                                   index=False, header=True, encoding='utf-8')

            # ... the best w.r.t. a kernel/datum.key type
            vector = best.properties.copy().iloc[best.index:(best.index + 1), :]
            vector.loc[:, 'key'] = datum.key
            vector.loc[:, 'method'] = datum.method
            vector.loc[:, 'datum'] = dict(datum._asdict())

            # Append
            excerpts.append(vector)

        # Concatenate ... this will have a model per kernel/key type
        excerpt = pd.concat(excerpts, axis=0, ignore_index=True)
        excerpt.to_csv(path_or_buf=os.path.join(self.directory, self.method + '.csv'),
                       index=False, header=True, encoding='utf-8')

        # Common steps ... this set of steps selects the best model from the best per kernel/key type
        index = excerpt['score'].idxmax()
        summary: pd.DataFrame = excerpt.iloc[index:(index + 1), :]
        summary.reset_index(drop=True, inplace=True)

        return summary
