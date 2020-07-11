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

    # Thinking ... calculations tree
    clustering.calculations.Calculations().exc()


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
    import clustering.calculations

    # Instances
    arguments = clustering.functions.arguments.Arguments()
    directories = clustering.functions.directories.Directories()
    unload = clustering.matrix.unload.Unload()
    read = clustering.matrix.read.Read()
    scale = clustering.matrix.scale.Scale()
    interface = clustering.projections.interface.Interface()

    main()
