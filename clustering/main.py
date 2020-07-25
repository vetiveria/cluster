import os
import sys


def main():
    # Ensure the data directories are empty, but exists
    directories.exc()

    # Unload data [parallel]
    unload.exc()

    # Read the data, and create a single design matrix [parallel]
    unscaled = read.exc()

    # Scale the data
    scale.exc(data=unscaled)

    # Thinking ... dimension reduction
    clustering.reduce.Reduce().exc()

    # Thinking ... cluster each projection ... kmc, gmm, bgmm
    clustering.cluster.Cluster().exc()


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
    import clustering.reductions.interface
    import clustering.reduce
    import clustering.cluster

    # Instances
    arguments = clustering.functions.arguments.Arguments()
    directories = clustering.functions.directories.Directories()
    unload = clustering.matrix.unload.Unload()
    read = clustering.matrix.read.Read()
    scale = clustering.matrix.scale.Scale()
    interface = clustering.reductions.interface.Interface()

    main()
