import collections
import os


# noinspection PyUnresolvedReferences,PyProtectedMember
class Config:

    def __init__(self):
        """
        The constructor
        """

        # Paths, Directories
        self.root = os.getcwd()
        self.warehouse = os.path.join(self.root, 'warehouse')
