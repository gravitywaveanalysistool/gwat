import numpy as np
from matplotlib import pyplot as plt

from src.graphing.graph import Graph


class XYGraph(Graph):
    def __init__(self, title, x, y, degree, x_label, y_label, best_fit, draw_lines):
        """
        @param title:
        @param x:
        @param y:
        @param degree:
        @param x_label:
        @param y_label:
        @param best_fit:
        @param draw_lines:
        """
        super().__init__(title)
        self.x = x
        self.y = y
        self.degree = degree
        self.x_label = x_label
        self.y_label = y_label
        self.best_fit = best_fit
        self.draw_lines = draw_lines

    def generate_graph(self, data, data_type):
        """
        Takes supplied data type generates a XYGraph based on supplied parameters

        Sets self.fig to the resulting figure

        @param data:
        @param data_type:
        @return:
        """
        fig = plt.figure()
        plt.plot(data[self.x], data[self.y], linewidth=3, label='Data Points', color='k')

        # Draw lines between dots if draw_lines is True
        if self.draw_lines:
            plt.plot(self.data[self.x], self.data[self.y], linestyle='-', color='k', alpha=0.5)

        # best fit curve
        if self.best_fit:
            coeffs = np.polyfit(data[self.y], data[self.x], self.degree)
            y_curve = np.linspace(data[self.y].min(), data[self.y].max(), 500)
            x_curve = np.polyval(coeffs, y_curve)
            plt.plot(x_curve, y_curve, 'r-', label='Best Fit Line')

        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)
        plt.legend()

        self._set_figure(fig, data_type)
        plt.close(fig)
