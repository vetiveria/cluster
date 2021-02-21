import numpy as np
import pandas as pd
import sklearn.decomposition
import cluster.functions.margin


class Kernel:

    def __init__(self):
        self.margin = cluster.functions.margin.Margin()
        self.random_state = 5

    @staticmethod
    def eigenstates(model: sklearn.decomposition.KernelPCA):

        eigenvalues = model.lambdas_
        components = np.arange(1, 1 + eigenvalues.shape[0])

        return pd.DataFrame(data={'component': components, 'eigenvalue': eigenvalues})

    def model(self, data) -> (np.ndarray, pd.DataFrame):

        # Decomposition: kernel -> 'rbf', 'cosine'
        algorithm = sklearn.decomposition.KernelPCA(kernel='rbf', eigen_solver='auto',
                                                    random_state=self.random_state)

        model: sklearn.decomposition.KernelPCA = algorithm.fit(data)

        # The transform
        transform = model.fit_transform(data)

        # The components and their eigenvalues
        eigenstates = self.eigenstates(model=model)

        return transform, eigenstates

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

    def exc(self, data: pd.DataFrame, exclude: list, identifier: str) -> (pd.DataFrame, pd.DataFrame):
        """

        :param data:
        :param exclude:
        :param identifier:
        :return:
        """

        # The independent variables
        regressors = data.columns.drop(labels=exclude)

        # Model
        transform, eigenstates = self.model(data=data[regressors])

        # Hence, plausible number of core principal components
        index, properties, field = self.margin.exc(values=eigenstates.eigenvalue.values)
        properties = eigenstates[['component']].join(properties)

        # Principals
        if np.isnan(index):
            principals = None
        else:
            limit = eigenstates.component[index]
            reference = data[identifier].values.reshape(data.shape[0], 1)
            principals = self.principals(reference=reference, transform=transform, limit=limit, identifier=identifier)

        return principals, properties, field
