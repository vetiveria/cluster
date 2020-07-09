import numpy as np
import pandas as pd


class Margin:
    """
    Estimates the
        * point of diminishing returns w.r.t. a sequence of points approaching an asymptote, or
        * first turning point of a curve
    outwith the first self.START points, i.e., starting from index self.START
    """

    def __init__(self):
        """
        The constructor
        """

        self.START = 2

    @staticmethod
    def differences(values: np.ndarray) -> np.ndarray:
        """

        :param values: An array of sequential values
        :return:
        """

        # The sequential differences
        return np.diff(
            np.concatenate((np.zeros(1), values), axis=0)
        )

    def extrema(self, properties: pd.DataFrame, field: str) -> int:
        """

        :param properties: Data
        :param field: The field about which minima & maxima will be determined
        :return:
        """
        minima = (properties.before > properties[field]) & (properties.after > properties[field])
        maxima = (properties.before < properties[field]) & (properties.after < properties[field])
        properties['extrema'] = minima | maxima

        indices = properties[properties.extrema == True].index
        index = indices[indices >= self.START].min()

        return index

    @staticmethod
    def bounds(properties, field):
        """

        :param properties:
        :param field:
        :return:
        """
        properties['before'] = pd.Series([0]).append(properties.iloc[:-1][field], ignore_index=True)
        properties['after'] = properties.iloc[1:][field].append(pd.Series([0]), ignore_index=True)

        return properties

    def exc(self, values: np.ndarray) -> (int, pd.DataFrame):
        """
        Estimates the knee+ point of a curve

        :param values: An array of sequential values
        :return:
        """

        derivatives = self.differences(values=values)
        characteristics = self.differences(values=derivatives)
        properties = pd.DataFrame(data={'score': values, 'derivatives': derivatives, 'characteristic': characteristics})

        # If true, inflection point approach
        state = (properties[self.START:].derivatives >= 0).all() | (properties[self.START:].derivatives <= 0).all()
        field = 'characteristic' if state else 'score'

        properties = self.bounds(properties, field)
        index = self.extrema(properties, field)

        return index, properties, field
