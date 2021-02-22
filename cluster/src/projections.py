import pandas as pd
import numpy as np

import collections

import config


# noinspection PyUnresolvedReferences,PyProtectedMember
class Projections:

    def __init__(self):

        # Configurations
        configurations = config.Config()
        self.locators, self.identifiers = configurations.projections_()
        self.descriptions = configurations.descriptions_()

        # Data Class
        self.Projection = collections.namedtuple(typename='Projection',
                                                 field_names=['frame', 'tensor', 'key', 'description'])

    def frame_(self, key: str) -> pd.DataFrame:
        """

        :return:
        """

        print(self.locators[key])

        try:
            data = pd.read_csv(filepath_or_buffer=self.locators[key],
                               header=0, encoding='UTF-8', dtype=self.identifiers)
        except OSError as err:
            raise Exception(err.strerror) from err

        return data

    def tensor_(self, frame: pd.DataFrame) -> np.ndarray:
        """

        :return:
        """

        return frame.drop(columns=list(self.identifiers.keys())).values

    def exc(self, key: str) -> collections.namedtuple:
        """

        :return:
        """

        frame = self.frame_(key=key)
        tensor = self.tensor_(frame=frame)

        return self.Projection._make((frame, tensor, key, self.descriptions[key]))
