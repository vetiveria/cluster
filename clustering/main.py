import argparse
import os
import sys


def main():

    # Parse the package's input
    arguments = clustering.functions.arguments.Arguments()
    parser = argparse.ArgumentParser()
    parser.add_argument('method', type=arguments.projector,
                        help='The dimensionality reduction method: PCA, KERNEL PCA')
    args = parser.parse_args()

    # Prepare directories
    directories = clustering.functions.directories.Directories()
    directories.exc()

    # Unload data
    unload = clustering.matrix.unload.Unload()
    unload.exc()

    # The unscaled design matrix ... next conditional return of scaled/unscaled
    # read = clustering.matrix.read.Read(data_=config.data_, attributes_=config.attributes_)
    # design = read.exc()
    # design.to_csv(path_or_buf='design.csv', header=True, index=False, encoding='UTF-8')


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'clustering'))

    # Libraries
    import config
    import clustering.matrix.unload
    import clustering.matrix.read
    import clustering.functions.arguments
    import clustering.functions.directories
    import clustering.projections.interface

    main()
