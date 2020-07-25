import dask
import numpy as np
import pandas as pd
import sklearn.mixture

import clustering.clusters.measures
import config


class BGMM:

    def __init__(self, principals, matrix_type):

        self.name = 'bayesian gaussian mixture model'
        self.array_covariance_type = np.array(['full', 'diag', 'tied', 'spherical'])
        self.marginal = 'likelihood'

        self.random_state = config.random_state
        self.array_of_k = config.array_of_k

        self.principals = principals
        self.matrix = self.principals.drop(columns=config.identifier).values
        self.matrix_type = matrix_type

    def modelling(self, n_components, covariance_type):

        try:
            model = sklearn.mixture.BayesianGaussianMixture(
                n_components=n_components, covariance_type=covariance_type, tol=0.001, reg_covar=1e-06, max_iter=100,
                n_init=1, init_params='kmeans', weight_concentration_prior_type='dirichlet_process',
                weight_concentration_prior=None, mean_precision_prior=None, mean_prior=None, degrees_of_freedom_prior=None,
                covariance_prior=None, random_state=self.random_state, warm_start=False, verbose=0, verbose_interval=10
            ).fit(X=self.matrix)
        except Exception as err:
            print(err)
            print('B.G.M.M. -> Skipping K: {}, Covariance Type: {}'.format(n_components, covariance_type))
            model = None

        return model

    def likelihood(self, models):

        likelihood_ = [[model.lower_bound_, model.covariance_type, model.n_components,
                        np.unique(model.predict(self.matrix)).shape[0]]
                       for model in models]

        return pd.DataFrame(data=likelihood_,
                            columns=['score', 'covariance_type', 'n_components', 'K'])

    @staticmethod
    def best(models, selection) -> sklearn.mixture.BayesianGaussianMixture:

        estimate_ = [model for model in models if ((model.n_components == selection.n_components)
                                                   & (model.covariance_type == selection.covariance_type))]

        return estimate_[0]

    def measurements(self, estimate: sklearn.mixture.BayesianGaussianMixture):

        measures = clustering.clusters.measures.Measures(self.principals)
        return measures.exc(labels=estimate.predict(self.matrix), matrix_type=self.matrix_type, model=self.name,
                            marginal=self.marginal, covariance=estimate.covariance_type)

    def exc(self):

        computations = [dask.delayed(self.modelling)(n_components=n_components, covariance_type=covariance_type)
                        for n_components in self.array_of_k for covariance_type in self.array_covariance_type]
        models = dask.compute(computations, scheduler='processes')[0]
        models = [model for model in models if model is not None]

        likelihood = self.likelihood(models=models)
        if likelihood.empty:
            estimate = None
            measurements = None
        else:
            estimate = self.best(models=models, selection=likelihood.loc[likelihood.score.idxmax()])
            measurements = self.measurements(estimate=estimate)

        return estimate, measurements
