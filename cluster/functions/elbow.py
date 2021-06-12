import cluster.src.projections

import sklearn.cluster
import yellowbrick.cluster

import logging


# noinspection PyUnresolvedReferences
class Elbow:

    def __init__(self):

        # Projections
        self.projections = cluster.src.projections.Projections()

        # Logging
        logging.basicConfig(level=logging.INFO, format='%(message)s%(asctime)s.%(msecs)03d', datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)

    def exc(self, datum):

        model = sklearn.cluster.KMeans()

        self.logger.info('Case {}, {}\n'.format(datum.key, datum.description))

        projection = self.projections.exc(datum=datum)

        visualizer = yellowbrick.cluster.KElbowVisualizer(
            model, k=(3, 13), metric='silhouette', timings=True, locate_elbow=True)
        visualizer.fit(X=projection.tensor)
        visualizer.show()

        print(visualizer.elbow_value_)
