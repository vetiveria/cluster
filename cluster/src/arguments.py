import requests
import yaml
import collections


class Arguments:

    def __init__(self):
        """
        Constructor
        """

    @staticmethod
    def url(urlstring) -> requests.models.Response:
        """
        Ascertains that the URL argument is valid
        :param urlstring: A URL string (to a YAML file)
        :return:
        """

        try:
            req = requests.get(url=urlstring)
            req.raise_for_status()
        except requests.exceptions.RequestException as err:
            raise err

        return req

    @staticmethod
    def parameters(elements: requests.models.Response) -> (str, dict, collections.namedtuple):
        """
        :param elements: The content of the input YAML file
        :return:
        """

        text = yaml.safe_load(elements.text)

        # The name of the data set/group
        group: str = text['group']

        # The details of the kernel matrices
        kernels: dict = text['kernels']

        # The details of the design matrix
        Design = collections.namedtuple(typename='Design', field_names=['dataURL', 'attributesURL'])
        design = Design._make((text['design']['url']['data'], text['design']['url']['attributes']))

        return group, kernels, design
