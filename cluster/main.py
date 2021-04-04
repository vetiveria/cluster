import logging
import os
import sys

import pandas as pd


def main():

    # Prepare
    directories.cleanup()
    directories.create()

    # Model
    selections = []
    supplements = []
    for method in ['kmc', 'bgmm', 'gmm']:
        # In focus
        logger.info('\n\n{}'.format(method))

        # Modelling
        selection, properties = interface.exc(method=method)

        # Combine then select the best, ... save required data
        selections.append(selection)
        supplements.append(properties)

    # The best ...
    frame = pd.concat(selections, axis=0, ignore_index=True)
    index = frame['score'].idxmax()
    logger.info('\n\n{}\n'.format(frame.loc[:, ['calinski', 'calinski_inverse', 'davies',  'density',
                                                'score', 'silhouette_median', 'silhouette_mean', 'method']]))

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
    logging.basicConfig(level=logging.INFO, format='%(message)s\n%(asctime)s.%(msecs)03d', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # Configurations
    import config

    configurations = config.Config()
    keys = configurations.keys
    descriptions: dict = configurations.descriptions_()

    # Libraries
    import cluster.model.interface
    import cluster.finale.prospects
    import cluster.src.directories

    interface = cluster.model.interface.Interface()
    directories = cluster.src.directories.Directories()

    main()
