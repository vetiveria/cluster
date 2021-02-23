import pandas as pd

import cluster.model.bgmm.interface
import cluster.model.kmc.interface


class Interface:

    def __init__(self):
        """

        """

        self.bgmm = cluster.model.bgmm.interface.Interface()
        self.kmc = cluster.model.kmc.interface.Interface()

    def exc(self, modelstr: str) -> pd.DataFrame:
        """

        :param modelstr:
        :return:
        """

        switch = {
            'bgmm': self.bgmm.exc(),
            'kmc': self.kmc.exc()
        }

        return switch.get(modelstr, LookupError("The model '{}' has not been implemented"))
