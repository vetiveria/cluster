import pandas as pd

import cluster.model.bgmm.interface
import cluster.model.kmc.interface
import cluster.model.gmm.interface
import cluster.model.sc.interface


class Interface:

    def __init__(self, group: str, kernels: dict, directory: str):
        """

        :param group: baseline?, cancer?, kidney?
        :param kernels: The metadata details of the kernel projections that would undergo clustering
        :param directory: The directory for the group's calculations
        """

        self.bgmm = cluster.model.bgmm.interface.Interface(group=group, kernels=kernels, directory=directory)
        self.kmc = cluster.model.kmc.interface.Interface(group=group, kernels=kernels, directory=directory)
        self.gmm = cluster.model.gmm.interface.Interface(group=group, kernels=kernels, directory=directory)
        self.sc = cluster.model.sc.interface.Interface(group=group, kernels=kernels, directory=directory)

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
