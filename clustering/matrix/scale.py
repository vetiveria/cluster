import pandas as pd
import sklearn.preprocessing

import config


class Scale:

    def __init__(self):
        self.exclude = config.exclude

    @staticmethod
    def standard(matrix: pd.DataFrame):
        return sklearn.preprocessing.StandardScaler().fit_transform(X=matrix)

    @staticmethod
    def robust(matrix: pd.DataFrame):
        return sklearn.preprocessing.RobustScaler().fit_transform(X=matrix)

    def exc(self, data: pd.DataFrame, method: str):
        values = data.drop(columns=self.exclude)

        matrix = {
            'robust': self.robust(matrix=values),
            'standard': self.standard(matrix=values)
        }.get(method, LookupError('Unknown scaling method - {}'.format(method)))

        scaled = pd.DataFrame(data=matrix, columns=data.columns.drop(labels=self.exclude))
        scaled = data[self.exclude].join(scaled)
        scaled.to_csv(path_or_buf='scaled.csv', header=True, index=False, encoding='UTF-8')

        return scaled
