import os
import sys

import pandas as pd

import logging


def main():

    selections = []
    supplements = []
    for method in ['kmc', 'gmm', 'bgmm']:

        # In focus
        logger.info('\n\n{}\n'.format(method))

        # Modelling
        selection, properties = interface.exc(method=method)

        # Combine then select the best, ... save required data
        selections.append(selection)
        supplements.append(properties)

    # The best ...
    frame = pd.concat(selections, axis=0, ignore_index=True)
    index = frame['score'].idxmax()

    # Hence
    details: pd.Series = frame.iloc[index, :]
    details.rename('details')
    supplements = supplements[index]

    cluster.finale.prospects.Prospects(details=details, supplements=supplements).exc()


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
    import cluster.finale.prospects

    # Instances
    configurations = config.Config()
    keys = configurations.keys
    descriptions: dict = configurations.descriptions_()

    interface = cluster.model.interface.Interface()


    main()
