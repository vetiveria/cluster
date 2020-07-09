import config

import clustering.projections.kernel
import clustering.projections.linear


class Interface:

    def __init__(self):

        self.algorithms = config.algorithms
        self.methods = list(self.algorithms.keys())

        self.exclude = config.exclude
        self.identifiers = config.identifiers

    def project(self, data, method):

        # Methods
        linear = clustering.projections.linear.Linear()
        kernel = clustering.projections.kernel.Kernel()

        # On failure
        failure = 'The string {method} is not a member of {methods}'

        # Reduction
        principals, properties, field = {
            self.algorithms['LINEAR PCA']: linear.exc(data=data, exclude=self.exclude, identifiers=self.identifiers),
            self.algorithms['KERNEL PCA']: kernel.exc(data=data, exclude=self.exclude, identifiers=self.identifiers)
        }.get(method, LookupError(failure.format(method=method, methods=self.methods)))

        return principals, properties, field

    def exc(self, data, method):

        return self.project(data=data, method=method)
