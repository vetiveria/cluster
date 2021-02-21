import argparse

import config


class Arguments:

    def __init__(self):
        self.methods = list(config.algorithms.keys())

    def projector(self, method: str):
        if method.lower() not in self.methods:
            raise argparse.ArgumentTypeError('The method must be a member of the list {}'.format(self.methods))

        return method.upper()
