import os
import sys
import argparse
import collections


def main():

    elbow = cluster.functions.elbow.Elbow()
    for key_, arg in kernels.items():

        datum = Datum._make((group, '', key_, arg['url'], arg['description'], arg['identifiers']))
        elbow.exc(datum=datum)


if __name__ == '__main__':

    # Preliminaries
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'clustering'))

    # Classes
    import cluster.functions.elbow
    import cluster.src.arguments

    """
    Datum
    """
    Datum = collections.namedtuple(typename='Datum',
                                   field_names=['group', 'method', 'key', 'url', 'description', 'identifiers'])

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
    group, kernels, design, original = arguments.parameters(elements=args.elements)

    main()
