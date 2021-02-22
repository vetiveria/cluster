import collections
import os


# noinspection PyUnresolvedReferences,PyProtectedMember
class Config:

    def __init__(self):
        self.root = os.getcwd()
        self.keys = ['linear', 'rbf', 'cosine']

    def descriptions_(self):
        Descriptions = collections.namedtuple(typename='Descriptions', field_names=self.keys)
        descriptions = Descriptions('Linear PCA', 'Radial Basis Function Kernel PCA', 'Cosine Kernel PCA')._asdict()

        return descriptions

    def projections_(self) -> (dict, dict):
        identifiers = {'COUNTYGEOID': str}

        url = 'https://raw.githubusercontent.com/vetiveria/segments/master/warehouse/principals/{}/projections.csv'
        URL = collections.namedtuple(typename='URL', field_names=self.keys)
        locators = URL._make((url.format('linear'), url.format('kernel/rbf'), url.format('kernel/cosine')))._asdict()

        return locators, identifiers

    @staticmethod
    def design_():
        url = 'https://raw.githubusercontent.com/vetiveria/segments/master/warehouse/design/{}.csv'
        URL = collections.namedtuple(typename='URL', field_names=['data', 'attributes'])
        locators = URL(**{'data': url.format('design'), 'attributes': url.format('attributes')})

        return locators