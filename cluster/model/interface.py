import pandas as pd

import cluster.model.bgmm.interface


class Interface:

    def __init__(self):
        """

        """

        self.bgmm = cluster.model.bgmm.interface.Interface()

    def exc(self, modelstr: str) -> pd.DataFrame:
        """

        :param modelstr:
        :return:
        """

        return {
            'bgmm': self.bgmm.exc()
        }.get(modelstr, LookupError("The model '{}' has not been implemented".format(modelstr)))
