import numpy as np
from matplotlib import pyplot as plt

from src.graphing.graph import Graph


class XYGraph(Graph):
    def __init__(self, title, data, x, y, degree, x_label, y_label, best_fit):
        super().__init__(title, data)
        self.x = x
        self.y = y
        self.degree = degree
        self.x_label = x_label
        self.y_label = y_label
        self.best_fit = best_fit

    def generate_graph(self):
        fig = plt.figure()
        plt.scatter(self.data[self.x], self.data[self.y], s=5, label='Data Points')

        # best fit curve
        coeffs = np.polyfit(self.data[self.y], self.data[self.x], self.degree)
        y_curve = np.linspace(self.data[self.y].min(), self.data[self.y].max(), 500)
        x_curve = np.polyval(coeffs, y_curve)

        if self.best_fit:
            plt.plot(x_curve, y_curve, 'r-', label='Best Fit Line')
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)
        plt.legend()

        self.fig = fig
