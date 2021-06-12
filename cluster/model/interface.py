import pandas as pd

import cluster.model.bgmm.interface
import cluster.model.kmc.interface
import cluster.model.gmm.interface
import cluster.model.sc.interface


class Interface:

    def __init__(self, group: str, kernels: dict):
        """
        Constructor
        """

        self.bgmm = cluster.model.bgmm.interface.Interface(group=group, kernels=kernels)
        self.kmc = cluster.model.kmc.interface.Interface(group=group, kernels=kernels)
        self.gmm = cluster.model.gmm.interface.Interface(group=group, kernels=kernels)
        self.sc = cluster.model.sc.interface.Interface(group=group, kernels=kernels)

    def exc(self, method: str) -> pd.DataFrame:
        """

        :param method: The clustering method
        :return:
        """

        if method == 'bgmm':
            summary = self.bgmm.exc()
        elif method == 'kmc':
            summary = self.kmc.exc()
        elif method == 'gmm':
            summary = self.gmm.exc()
        elif method == 'sc':
            summary = self.sc.exc()
        else:
            raise Exception("The method '{}' has not been implemented".format(method))

        return summary
