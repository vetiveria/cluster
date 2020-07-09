import argparse

import config


class Arguments:

    def __init__(self):
        self.name = ''
        self.methods = config.methods

    def projector(self, method: str):
        if method.upper() not in self.methods:
            raise argparse.ArgumentTypeError('The method must be a member of the list {}'.format(self.methods))

        return method.upper()
