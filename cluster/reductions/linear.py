import numpy as np
import pandas as pd
import sklearn.decomposition

import cluster.functions.margin


class Linear:

    def __init__(self):
        self.margin = cluster.functions.margin.Margin()
        self.random_state = 5

    @staticmethod
    def variance(model: sklearn.decomposition.PCA) -> pd.DataFrame:
        """
        The dimensionality reduction model; PCA.

        :param model: The PCA projections

        :return:
        """

        discrete = model.explained_variance_ratio_
        explain = discrete.cumsum()
        components = np.arange(start=1, stop=1 + model.n_components_)
        return pd.DataFrame(data={'components': components, 'explain': explain,
                                  'discrete': discrete})

    def model(self, data):

        # Decomposition
        pca = sklearn.decomposition.PCA(n_components=None, svd_solver='full', random_state=self.random_state)
        model: sklearn.decomposition.PCA = pca.fit(data)

        # The transform
        transform = model.fit_transform(data)

        # The variance explained by the decomposition components
        variance: pd.DataFrame = self.variance(model=model)

        return transform, variance

    @staticmethod
    def principals(reference: np.ndarray, transform: np.ndarray, limit: int, identifier: str) -> pd.DataFrame:

        # The critical components
        core = transform[:, :limit].copy()

        # Fields
        fields = ['C{:02d}'.format(i) for i in np.arange(1, 1 + limit)]
        fields = [identifier] + fields

        # values
        values = np.concatenate((reference, core), axis=1)

        return pd.DataFrame(data=values, columns=fields)

    def exc(self, data: pd.DataFrame, exclude: list, identifier: str) -> (pd.DataFrame, pd.DataFrame, str):

        # The independent variables
        regressors = data.columns.drop(labels=exclude)

        # Model
        transform, variance = self.model(data[regressors])

        # Hence, plausible number of core principal components
        index, properties, field = self.margin.exc(values=variance.discrete.values)
        properties = variance[['components', 'explain']].join(properties)

        # Principals
        if np.isnan(index):
            principals = None
        else:
            limit = variance.components[index]
            reference = data[identifier].values.reshape(data.shape[0], 1)
            principals = self.principals(reference=reference, transform=transform, limit=limit, identifier=identifier)

        return principals, properties, field
