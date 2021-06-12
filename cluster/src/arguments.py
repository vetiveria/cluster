import requests
import yaml
import collections


class Arguments:

    def __init__(self):
        """

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
    def parameters(elements: requests.models.Response):
        """
        :param elements: The content of the input YAML file
        :return:
        """

        text = yaml.safe_load(elements.text)

        ProjectionsURL = collections.namedtuple(typename='ProjectionsURL', field_names=['rbf', 'cosine'])
        url = ProjectionsURL._make((text['projections']['url']['rbf'], text['projections']['url']['cosine']))

        ProjectionsDescription = collections.namedtuple(typename='ProjectionsDescription', field_names=['rbf', 'cosine'])
        description = ProjectionsDescription._make(
            (text['projections']['description']['rbf'], text['projections']['description']['cosine']))

        return text['group'], url, description
