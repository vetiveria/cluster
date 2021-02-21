import glob
import os

import pandas as pd

import config
import cluster.clusters.kmc
import cluster.clusters.bgmm


class Cluster:

    def __init__(self):

        self.path_principals = config.path_principals
        self.path_principals_attributes = config.path_principals_attributes

    def files(self):

        filestrings = glob.glob(os.path.join(self.path_principals, '*.csv'))
        filenames = [os.path.basename(filestring) for filestring in filestrings]

        return filestrings, filenames

    def attributes(self, filename):

        try:
            values = pd.read_csv(filepath_or_buffer=os.path.join(self.path_principals_attributes, filename),
                                 usecols=['field', 'type'], header=0, encoding='UTF-8')
        except OSError as err:
            raise err

        types = values.set_index(keys='field', drop=True).to_dict(orient='dict')['type']

        return types

    @staticmethod
    def matrix_type(filename):

        name = os.path.splitext(filename)[0]
        parts = name.split('_')
        return ' '.join(parts)

    def read(self, filestring: str, filename: str):

        try:
            principals = pd.read_csv(filepath_or_buffer=filestring, header=0,
                                     encoding='UTF-8', dtype=self.attributes(filename=filename))
        except OSError as err:
            raise err

        return principals

    def exc(self):

        filestrings, filenames = self.files()

        listing = pd.DataFrame()

        for filestring, filename in zip(filestrings, filenames):

            principals = self.read(filestring=filestring, filename=filename)
            matrix_type = self.matrix_type(filename)

            # The estimated cluster settings per clustering method requires a parallellel analysis via DASK, hence
            # avoid parallel analysis elsewhere, w.r.t. this section
            kmc = cluster.clusters.kmc.KMC(principals=principals, matrix_type=matrix_type)
            bgmm = cluster.clusters.bgmm.BGMM(principals=principals, matrix_type=matrix_type)

            for i in [kmc, bgmm]:
                estimate, measurements = i.exc()
                measurements['estimate'] = estimate
                listing = pd.concat((listing, measurements), ignore_index=True, axis=0)

        print(listing)
