import numpy as np
import pandas as pd

import collections


class Underlying:

    def __init__(self, source: collections.namedtuple):
        """

        :param source: fields ->['dataURL', 'attributesURL', 'identifiers']
        """

        self.attributes_url = source.attributesURL
        self.data_url = source.dataURL
        self.identifiers = source.identifiers

        self.DataCollection = collections.namedtuple(typename='DataCollection', field_names=['frame', 'tensor'])

    def attributes(self):
        """

        :return:
        """

        try:
            data = pd.read_csv(self.attributes_url, header=0, encoding='UTF-8')
        except OSError as err:
            raise ("OS Error: {0}".format(err))

        fields = data.field.to_list()
        types = data[['field', 'type']].set_index(keys='field').to_dict(orient='dict')['type']

        return fields, types

    def frame_(self):
        """

        :return:
        """

        fields, types = self.attributes()

        try:
            data = pd.read_csv(filepath_or_buffer=self.data_url, usecols=fields,
                               header=0, encoding='UTF-8', dtype=types)
        except OSError as err:
            raise Exception(err.strerror) from err

        return data

    def exc(self):
        """

        :return:
        """

        frame: pd.DataFrame = self.frame_()
        tensor: np.ndarray = frame.drop(columns=list(self.identifiers.keys())).values

        return self.DataCollection._make((frame, tensor))
