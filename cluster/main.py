import os
import sys

import logging


def main():

    for key in keys:

        # In focus
        logger.info('\n{}\nModelling the {} projections\n'.format(key, descriptions[key]))

        # Projection
        projection = projections.exc(key=key)
        logger.info('{}\n'.format(projection.frame.head()))

        # The determined models ...


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'clustering'))

    # Logging
    logging.basicConfig(level=logging.INFO, format='%(message)s%(asctime)s.%(msecs)03d', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # Libraries
    import config

    import cluster.src.projections

    # Instances
    configurations = config.Config()
    keys = configurations.keys
    descriptions = configurations.descriptions_()

    projections = cluster.src.projections.Projections()

    main()
