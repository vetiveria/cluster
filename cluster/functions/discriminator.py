import collections

import pandas as pd


class Discriminator:

    def __init__(self):
        """

        """

        self.variables = ['calinski_inverse', 'davies', 'density']
        self.Best = collections.namedtuple(typename='Best', 
                                           field_names=['properties', 'index', 'estimate', 'discriminant'])

    @staticmethod
    def score(blob):
        """
        
        :return:
        """

        scores = (blob['density'] - blob[['calinski_inverse', 'davies']].sum(axis=1)).astype('float64')

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

        # Hence, use the scaled variables to calculate each record's score
        scores = pd.DataFrame(data={'score': self.score(blob=determinants)})
        properties = pd.concat((determinants, scores), axis=1)
        
        return self.best(properties=properties)
