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

    def exc(self, method: str) -> pd.DataFrame:
        """

        :param method:
        :return:
        """

        if method == 'bgmm':
            summary = self.bgmm.exc(method=method)
        elif method == 'kmc':
            summary = self.kmc.exc(method=method)
        elif method == 'gmm':
            summary = self.gmm.exc(method=method)
        elif method == 'sc':
            summary = self.sc.exc(method=method)
        else:
            raise Exception("The method '{}' has not been implemented".format(method))

        return summary
