import numpy as np
import pandas as pd

import collections


class Design:

    def __init__(self, design: collections.namedtuple):
        """
        The constructor

        """

        self.attributes_url = design.attributesURL
        self.data_url = design.dataURL
        self.identifiers = design.identifiers

        self.DesignCollection = collections.namedtuple(typename='DesignCollection', field_names=['frame', 'tensor'])

    def attributes(self):
        """

        :return:
        """

        try:
            data = pd.read_csv(self.attributes_url, header=0, encoding='UTF-8')
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

        return self.DesignCollection._make((frame, tensor))
