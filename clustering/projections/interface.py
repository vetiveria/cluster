import config

import clustering.projections.kernel
import clustering.projections.linear


class Interface:

    def __init__(self):

        self.methods = config.methods

    def exc(self, data, method):

        # Methods
        linear = clustering.projections.linear.Linear()
        kernel = clustering.projections.kernel.Kernel()

        # Reduction
        failure = 'The string {method} is not a member of {methods}'
        principals, properties, field = {
            'PCA': linear.exc(data=data, exclude=['COUNTYGEOID'], identifiers=['COUNTYGEOID']),
            'KERNEL PCA': kernel.exc(data=data, exclude=['COUNTYGEOID'], identifiers=['COUNTYGEOID'])
        }.get(method, LookupError(failure.format(method=method, methods=self.methods)))

        return principals, properties, field
