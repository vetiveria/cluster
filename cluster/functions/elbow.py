import cluster.src.projections

import config

import sklearn.cluster
import yellowbrick.cluster

import logging


class Elbow:

    def __init__(self):

        # Config
        configurations = config.Config()
        self.keys = configurations.keys
        self.descriptions = configurations.descriptions_()

        # Projections
        self.projections = cluster.src.projections.Projections()

        # Logging
        logging.basicConfig(level=logging.INFO, format='%(message)s%(asctime)s.%(msecs)03d', datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)

    def exc(self):

        model = sklearn.cluster.KMeans()

        for key in self.keys:

            self.logger.info('Case {}, {}\n'.format(key, self.descriptions[key]))

            projection = self.projections.exc(key=key)

            visualizer = yellowbrick.cluster.KElbowVisualizer(
                model, k=(3, 13), metric='silhouette', timings=True, locate_elbow=True)
            visualizer.fit(X=projection.tensor)
            visualizer.show()

            print(visualizer.elbow_value_)





