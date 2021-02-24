import pandas as pd

import cluster.model.bgmm.interface
import cluster.model.kmc.interface
import cluster.model.gmm.interface
import cluster.model.sc.interface


class Interface:

    def __init__(self):
        """

        """

        self.bgmm = cluster.model.bgmm.interface.Interface()
        self.kmc = cluster.model.kmc.interface.Interface()
        self.gmm = cluster.model.gmm.interface.Interface()
        self.sc = cluster.model.sc.interface.Interface()

    def exc(self, modelstr: str) -> pd.DataFrame:
        """

        :param modelstr:
        :return:
        """

        if modelstr == 'bgmm':
            summary = self.bgmm.exc()
        elif modelstr == 'kmc':
            summary = self.kmc.exc()
        elif modelstr == 'gmm':
            summary = self.gmm.exc()
        elif modelstr == 'sc':
            summary = self.sc.exc()
        else:
            raise Exception("The model '{}' has not been implemented".format(modelstr))

        return summary
