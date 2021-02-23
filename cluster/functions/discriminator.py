import collections

import sklearn.mixture
import sklearn.preprocessing

import numpy as np
import pandas as pd

import dask


class Discriminator:

    def __init__(self):
        """

        """

        self.variables = ['calinski', 'davies_transform', 'density']
        self.variables_scaled = ['scaled_' + i for i in self.variables]

        self.Best = collections.namedtuple(typename='Best', 
                                           field_names=['properties', 'index', 'estimate', 'discriminant'])

    @staticmethod
    def scale_(series):
        """
        
        :return:
        """

        array = series.values[:, None]
        scaler = sklearn.preprocessing.StandardScaler(with_mean=True, with_std=True).fit(array)
        scaled = pd.Series(np.squeeze(scaler.transform(array)), name='scaled_' + series.name)

        return scaled    

    def scale(self, determinants: pd.DataFrame):
        """
        
        :return:
        """

        calculations = [dask.delayed(self.scale_)(determinants[variable]) for variable in self.variables]
        dask.visualize(calculations, filename='scale', format='pdf')
        
        values = dask.compute(calculations, scheduler='processes')[0]
        table = pd.concat(values, axis=1)

        return table

    def score(self, blob):
        """
        
        :return:
        """

        scores = blob[self.variables_scaled].sum(axis=1)

        return scores

    def best(self, properties: pd.DataFrame):
        """

        :param properties:
        :return:
        """

        index = properties['score'].idxmax()
        return self.Best(properties=properties, 
                         index=index, 
                         estimate=properties.iloc[index, :]['model'], 
                         discriminant='derived score')

    def exc(self, determinants: pd.DataFrame):
        """
        
        :return:
        """

        # Scale the determinants' variables of interest; the scaled variables are concatenated to determinants
        features = self.scale(determinants=determinants)

        # Hence, use the scaled variables to calculate each record's score
        features.loc[:, 'score'] = self.score(blob=features)
        properties = pd.concat((determinants, features), axis=1)
        
        return self.best(properties=properties)
