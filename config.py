import collections
import os


# noinspection PyUnresolvedReferences,PyProtectedMember
class Config:

    def __init__(self):
        """
        The constructor
        """

        self.root = os.getcwd()
        self.warehouse = os.path.join(self.root, 'warehouse')
        self.directories = [self.warehouse]

        self.keys = ['rbf', 'cosine']

    def descriptions_(self):
        """

        :return:
        """

        Descriptions = collections.namedtuple(typename='Descriptions', field_names=self.keys)
        descriptions = Descriptions('Radial Basis Function Kernel PCA', 'Cosine Kernel PCA')._asdict()

        return descriptions

    def projections_(self) -> (dict, dict):
        """
        For the projection matrices section of the prospective YAML

        :return:
        """

        identifiers = {'COUNTYGEOID': str}

        url = 'https://raw.githubusercontent.com/vetiveria/segments/master/warehouse/principals/{}/projections.csv'
        URL = collections.namedtuple(typename='URL', field_names=self.keys)
        locators = URL._make((url.format('kernel/rbf'), url.format('kernel/cosine')))._asdict()

        return locators, identifiers

    @staticmethod
    def design_():
        """
        For the design matrix section of the prospective YAML

        :return:
        """

        identifiers = {'COUNTYGEOID': str}

        url = 'https://raw.githubusercontent.com/vetiveria/segments/master/warehouse/design/{}.csv'
        URL = collections.namedtuple(typename='URL', field_names=['data', 'attributes'])
        locators = URL(**{'data': url.format('design'), 'attributes': url.format('attributes')})

        return locators, identifiers
