import os
import sys

import pandas as pd

import logging


def main():

    for k, v in descriptions.items():

        # In focus
        logger.info(' {} Modelling\n'.format(v))

        inbrief: pd.DataFrame = interface.exc(modelstr=k)
        logger.info(' The best models of {}\n{}\n'.format(k, inbrief))


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'clustering'))

    # Logging
    logging.basicConfig(level=logging.INFO, format='%(message)s%(asctime)s.%(msecs)03d', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # Libraries
    import config

    import cluster.model.interface

    # Instances
    configurations = config.Config()
    keys = configurations.keys
    descriptions: dict = configurations.descriptions_()

    interface = cluster.model.interface.Interface()

    main()
