import argparse
import os
import sys


def main():

    # Parse the package's input (... use list(config.algorithms.keys()) )
    arguments = clustering.functions.arguments.Arguments()
    parser = argparse.ArgumentParser()
    parser.add_argument('method', type=arguments.projector,
                        help='The dimensionality reduction method: LINEAR PCA, KERNEL PCA')
    args = parser.parse_args()

    # Prepare directories
    directories = clustering.functions.directories.Directories()
    directories.exc()

    # Unload data
    unload = clustering.matrix.unload.Unload()
    unload.exc()

    # Design matrices
    read = clustering.matrix.read.Read()
    unscaled = read.exc()
    scale = clustering.matrix.scale.Scale()
    scaled = scale.exc(data=unscaled, method='robust')

    # Principals
    interface = clustering.projections.interface.Interface()
    principals, properties, field = interface.exc(data=scaled, method=args.method)
    print(principals.head())


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'clustering'))

    # Libraries
    import clustering.matrix.unload
    import clustering.matrix.read
    import clustering.matrix.scale
    import clustering.functions.arguments
    import clustering.functions.directories
    import clustering.projections.interface

    main()
