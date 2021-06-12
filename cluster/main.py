import logging
import os
import sys
import argparse

import pandas as pd


def main():

    # Prepare
    directories.cleanup()
    directories.create()

    # Model
    selections = []
    for method in ['kmc', 'bgmm', 'gmm']:

        # In focus
        logger.info('\n\n{}'.format(method))

        # Modelling
        selection = interface.exc(method=method)

        # Combine then select the best, ... save required data
        selections.append(selection)

    # Structure
    frame = pd.concat(selections, axis=0, ignore_index=True)
    logger.info('\n\n{}\n'.format(frame.loc[:, ['calinski', 'calinski_inverse', 'davies',  'density',
                                                'score', 'silhouette_median', 'silhouette_mean', 'method']]))

    # The best ...
    index = frame['score'].idxmax()
    details: pd.Series = frame.iloc[index, :]
    details.rename('details')

    # Save, cluster.finale.prospects...
    print(details)


if __name__ == '__main__':

    # Preliminaries
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'clustering'))

    # Logging
    logging.basicConfig(level=logging.INFO, format='%(message)s\n%(asctime)s.%(msecs)03d', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # Libraries
    import cluster.model.interface
    import cluster.finale.prospects
    import cluster.src.directories
    import cluster.src.arguments

    """
    Address arguments:
        The argument is a YAML URL, which outlines the parameters of the data that 
        would undergo clustering. 
    """
    # Parsing and processing arguments
    arguments = cluster.src.arguments.Arguments()
    parser = argparse.ArgumentParser()
    parser.add_argument('elements', type=arguments.url,
                        help='The URL of a YAML of parameters; refer to the README notes.  The argument '
                             'parser returns a blob of elements')
    args = parser.parse_args()

    # Get the data parameters encoded
    group, kernels, _ = arguments.parameters(elements=args.elements)

    """
    Instances
    """
    # Instances
    interface = cluster.model.interface.Interface(group=group, kernels=kernels)
    directories = cluster.src.directories.Directories()

    main()
