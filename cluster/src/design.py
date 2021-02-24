import pandas as pd
import numpy as np

import collections

import config


# noinspection PyUnresolvedReferences,PyProtectedMember
class Design:

    def __init__(self):
        """
        The constructor

        """

        configurations = config.Config()
        self.url, self.identifiers = configurations.design_()

        self.DesignCollection = collections.namedtuple(typename='DesignCollection', field_names=['frame', 'tensor'])

    def attributes(self):
        """

        :return:
        """

        try:
            data = pd.read_csv(self.url.attributes, header=0, encoding='UTF-8')
        except OSError as err:
            raise ("OS Error: {0}".format(err))

        # For 'usecols' & 'dtype', of the data to be read, respectively
        fields = data.field.to_list()
        types = data[['field', 'type']].set_index(keys='field').to_dict(orient='dict')['type']

        return fields, types

    def frame_(self):
        """

        :return:
        """

        try:
            data = pd.read_csv(filepath_or_buffer=self.url.data,
                               header=0, encoding='UTF-8', dtype=self.identifiers)
        except OSError as err:
            raise Exception(err.strerror) from err

        return data

    def tensor_(self, frame: pd.DataFrame) -> np.ndarray:
        """

        :return:
        """

        return frame.drop(columns=list(self.identifiers.keys())).values

    def exc(self):
        """

        :return:
        """

        frame = self.frame_()
        tensor = self.tensor_(frame=frame)

        return self.DesignCollection._make((frame, tensor))
