import collections
import os

import numpy as np
import pandas as pd

import cluster.src.underlying
import cluster.src.projections
import cluster.src.directories


class Prospects:

    def __init__(self, details: pd.Series, source: collections.namedtuple, directory: str):
        """
        Constructor
        :param details:
        :param source:
        :param directory:
        """

        # Preliminaries
        self.details = details
        self.source = source
        self.directory = directory

        # Datum
        Datum = collections.namedtuple(typename='Datum',
                                       field_names=['group', 'method', 'key', 'url', 'description', 'identifiers'])
        self.datum = Datum._make((details.group, details.method, details.key, details.url, details.keydesc,
                                  details.identifiers))

        # Instances
        self.projections = cluster.src.projections.Projections()
        self.directories = cluster.src.directories.Directories()

    def labels_(self, matrix) -> np.ndarray:
        """
        Gets the label of each record/instance
        :param matrix: The labels of this matrix will be extracted/determined
        :return:
        """

        if self.details.method == 'sc':
            labels: np.ndarray = self.details.model.labels_
        else:
            labels: np.ndarray = self.details.model.predict(matrix)

        return labels

    def releases_(self, labels):
        """
        Saves the underlying releases data
        :return:
        """

        # Original
        underlying = cluster.src.underlying.Underlying(source=self.source).exc()
        original: pd.DataFrame = underlying.frame
        original.loc[:, 'label'] = labels

        melted = original.melt(id_vars=['COUNTYGEOID', 'label'], var_name='tri_chem_id', value_name='quantity_kg')
        assert melted[['COUNTYGEOID', 'label']].drop_duplicates().shape[0] == \
            melted[['COUNTYGEOID']].drop_duplicates().shape[0], "Imbalanced releases data"

        # Releases per determined cluster
        for i in melted['label'].unique():
            frame = melted[melted['label'] == i]
            self.write(blob=frame, sections=['releases', '{:02d}.csv'.format(i)])

        # Reduced releases
        releases = melted[melted['quantity_kg'] > 0].copy()
        self.write(blob=releases, sections=['releases.csv'])

    def write(self, blob: pd.DataFrame, sections: list):
        """
        Write
        :param blob: The DataFrame that will be written to disc
        :param sections: The name of the file, including its extension
        :return:
        """

        filestring = os.path.join(self.directory, *sections)
        path = os.path.split(filestring)[0]
        self.directories.create(directories_=[path])

        blob.to_csv(path_or_buf=filestring, index=False, header=True,
                    encoding='UTF-8')

    def exc(self):
        """
        Weights: All data values are in kilograms, ref.
            https://github.com/vetiveria/spots/blob/master/src/releases/helpers.py#L52

        :return:
        """

        projection: collections.namedtuple = self.projections.exc(datum=self.datum)
        labels: np.ndarray = self.labels_(matrix=projection.tensor)

        # Principals
        principals: pd.DataFrame = projection.frame
        principals.loc[:, 'label'] = labels
        self.write(blob=principals, sections=['principals.csv'])

        # Releases
        self.releases_(labels=labels)
