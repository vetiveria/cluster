import os
import sys


def main():

    elbow = cluster.functions.elbow.Elbow()
    elbow.exc()


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'clustering'))

    import cluster.functions.elbow

    main()
