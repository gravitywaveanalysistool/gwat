import numpy as np
from matplotlib import pyplot as plt

from src.graphing.graph import Graph


class XYGraph(Graph):
    def __init__(self, title, data, x, y, degree, x_label, y_label, best_fit, draw_lines):
        super().__init__(title, data)
        self.x = x
        self.y = y
        self.degree = degree
        self.x_label = x_label
        self.y_label = y_label
        self.best_fit = best_fit
        self.draw_lines = draw_lines

    def generate_graph(self):
        fig = plt.figure()
        plt.scatter(self.data[self.x], self.data[self.y], s=5, label='Data Points')

        # Draw lines between dots if draw_lines is True
        if self.draw_lines:
            plt.plot(self.data[self.x], self.data[self.y], linestyle='-', color='b', alpha=0.5)

        # best fit curve
        if self.best_fit:
            coeffs = np.polyfit(self.data[self.y], self.data[self.x], self.degree)
            y_curve = np.linspace(self.data[self.y].min(), self.data[self.y].max(), 500)
            x_curve = np.polyval(coeffs, y_curve)
            plt.plot(x_curve, y_curve, 'r-', label='Best Fit Line')

        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)
        plt.legend()

        self.fig = fig
        plt.close(fig)
