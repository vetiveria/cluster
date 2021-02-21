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
    cluster.reduce.Reduce().exc()

    # Thinking ... cluster each projection ... kmc, gmm, bgmm
    cluster.cluster.Cluster().exc()


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'clustering'))

    # Libraries
    import cluster.matrix.unload
    import cluster.matrix.read
    import cluster.matrix.scale
    import cluster.functions.arguments
    import cluster.functions.directories
    import cluster.reductions.interface
    import cluster.reduce
    import cluster.cluster

    # Instances
    arguments = cluster.functions.arguments.Arguments()
    directories = cluster.functions.directories.Directories()
    unload = cluster.matrix.unload.Unload()
    read = cluster.matrix.read.Read()
    scale = cluster.matrix.scale.Scale()
    interface = cluster.reductions.interface.Interface()

    main()
