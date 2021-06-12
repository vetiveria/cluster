import pandas as pd
import numpy as np

import collections


class Projections:

    def __init__(self):
        """
        Constructor
        """

        # Data Class
        self.Projection = collections.namedtuple(typename='Projection',
                                                 field_names=['frame', 'tensor'])

    @staticmethod
    def frame_(datum: collections.namedtuple) -> pd.DataFrame:
        """

        :param datum: Note that datum.identifiers is a dict - field name & field data type pairs - that ensures that
        the identifier fields are read-in correctly
        :return:
        """

        try:
            data = pd.read_csv(filepath_or_buffer=datum.url, header=0, encoding='UTF-8', dtype=datum.identifiers)
        except OSError as err:
            raise Exception(err.strerror) from err

        return data

    def exc(self, datum: collections.namedtuple) -> collections.namedtuple:
        """
        Notes
            group -> baseline, cancer, kidney, or ...
            key -> rbf, cosine, or ...

        :param datum: fields -> [group, key, url, description, identifiers]
        :return:
        """

        # group, key, url, description, identifiers
        frame: pd.DataFrame = self.frame_(datum=datum)
        tensor: np.ndarray = frame.drop(columns=datum.identifiers.keys).values

        return self.Projection._make((frame, tensor))
