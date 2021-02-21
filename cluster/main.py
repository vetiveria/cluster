import os
import sys


def main():

    # Unload data [parallel]
    unload.exc()

    # Read the data, and create a single design matrix [parallel]
    unscaled = read.exc()

    # Scale the data
    scale.exc(data=unscaled)


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'clustering'))

    # Libraries
    import cluster.src.unload
    import cluster.src.read
    import cluster.src.scale

    unload = cluster.src.unload.Unload()
    read = cluster.src.read.Read()
    scale = cluster.src.scale.Scale()

    main()
