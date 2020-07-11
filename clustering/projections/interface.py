import pandas as pd
import os

import clustering.projections.kernel
import clustering.projections.linear
import config


class Interface:

    def __init__(self):

        self.path_principals = config.path_principals
        self.path_principals_attributes = config.path_principals_attributes

        self.algorithms = config.algorithms
        self.projection_methods = list(self.algorithms.keys())

        self.exclude = config.exclude
        self.identifier = config.identifier

    def error_message(self, projection_method):

        base = 'The string {projection_method} is not a member of {projection_methods}'

        return base.format(projection_method=projection_method,
                           projection_methods=self.projection_methods)

    def project(self, data, projection_method) -> (pd.DataFrame, pd.DataFrame, str):

        # Methods
        linear = clustering.projections.linear.Linear()
        kernel = clustering.projections.kernel.Kernel()

        # Reduction
        principals, properties, field = {
            self.algorithms['linear']: linear.exc(data=data, exclude=self.exclude, identifier=self.identifier),
            self.algorithms['kernel']: kernel.exc(data=data, exclude=self.exclude, identifier=self.identifier)
        }.get(projection_method, LookupError(self.error_message(projection_method=projection_method)))

        return principals, properties, field

    def attr(self, fields, filename):

        setup = pd.DataFrame(data={'field': fields})
        condition = setup.field == self.identifier
        
        setup['type'] = 'float'
        setup.loc[condition, 'type'] = 'str'

        setup.to_csv(path_or_buf=os.path.join(self.path_principals_attributes, filename),
                     header=True, index=False, encoding='UTF-8')

    def exc(self, matrix,  matrix_type, projection_method) -> str:

        # The principal components, and supplementary materials
        principals, properties, field = self.project(data=matrix, projection_method=projection_method)

        # Saving the principals
        if principals is not None:

            filename = '{matrix_type}{projection_method}.csv'.format(matrix_type=matrix_type,
                                                                     projection_method=projection_method)
            principals.to_csv(path_or_buf=os.path.join(self.path_principals, filename),
                              header=True, index=False, encoding='UTF-8')

            self.attr(principals.columns, filename)

            return 'Success: {}, {}'.format(matrix_type, projection_method)

        else:

            return 'impossible'
