"""
Module graphs

"""
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

class Graphs:
    """
    Class Graphs

    """

    def __init__(self):
        """
        The constructor

        """
        
        sns.set_style("darkgrid")
        sns.set_context("poster")
        sns.set(font_scale=0.75)

    @staticmethod
    def scatter(data: pd.DataFrame, x: str, y: str, labels: dict, hue: str=None):
        """

        :param data: A DataFrame
        :param x: The abscissae field
        :param y: The ordinates field
        :param labels: The dictionary of x & y axis labels
        :param hue: For differentiating

        :return:
        """
        plt.figure(figsize=(4.8, 2.9))
        plt.tick_params(axis='both', labelsize='large')

        sns.scatterplot(x=x, y=y, data=data, hue=hue)

        plt.xlabel(labels['x'], fontsize='large')
        plt.ylabel(labels['y'], fontsize='large')
