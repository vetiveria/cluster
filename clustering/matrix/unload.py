import io
import os
import urllib.request
import zipfile

import dask
import requests

import config


class Unload:

    def __init__(self):
        """
        The constructor
        """

        self.data_urlstrings = config.data_urlstrings
        self.attributes_urlstring = config.attributes_urlstring

        self.data_path = config.data_path
        self.attributes_path = config.attributes_path

    def attributes(self):

        urllib.request.urlretrieve(self.attributes_urlstring,
                                   os.path.join(self.attributes_path, os.path.basename(self.attributes_urlstring)))

    @staticmethod
    def read(urlstring: str) -> bytes:
        """

        :param urlstring: The URL of the archived file that would be de-archived locally
        :return: The file contents, in byte form
        """

        try:
            req = requests.get(url=urlstring)
            req.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise e

        return req.content

    def unzip(self, urlstring: str):
        """
        De-archives a zip archive file
        :param urlstring:
        :return:
        """

        obj = zipfile.ZipFile(io.BytesIO(self.read(urlstring=urlstring)))
        obj.extractall(path=self.data_path)

    def exc(self):
        """

        :return:
        """

        self.attributes()

        computations = [dask.delayed(self.unzip)(urlstring) for urlstring in self.data_urlstrings]
        dask.visualize(computations, filename='unload', format='pdf')
        dask.compute(computations, scheduler='processes')
