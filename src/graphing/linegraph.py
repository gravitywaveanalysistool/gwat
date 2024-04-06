import matplotlib.pyplot as plt
import numpy as np

from src.graphing.graph import Graph


class LineGraph(Graph):
    def __init__(self, title, x, y, degree, x_label, y_label, best_fit):
        super().__init__(title)
        self.x = x
        self.y = y
        self.degree = degree
        self.x_label = x_label
        self.y_label = y_label
        self.best_fit = best_fit

    def generate_graph(self, data, data_type):
        fig = plt.figure(layout='tight')

        # Assuming self.data[self.x] contains x-axis data and self.data[self.y] contains y-axis data
        x = data[self.x]
        y = data[self.y]

        # Skip every nth point (e.g., every 5th point)
        skip = 2

        # Plot the data points with skipping
        plt.scatter(x[::skip], y[::skip], s=5, label='Data Points', color='k')

        # Smooth the y-axis data using a moving average
        window_size = 5  # Adjust window size as needed
        smoothed_y = data[self.y].rolling(window=window_size, min_periods=1).mean()
        smoothed_x = data[self.x].rolling(window=window_size, min_periods=1).mean()

        # Plot the smoothed line graph
        plt.plot(smoothed_x, smoothed_y, label='Smoothed Line', color='r')

        # best fit curve
        if self.best_fit:
            coeffs = np.polyfit(y, x, self.degree)
            y_curve = np.linspace(min(y), max(y), 500)
            x_curve = np.polyval(coeffs, y_curve)
            plt.plot(x_curve, y_curve, 'r-', label='Best Fit Line')

        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self._graph_title(data_type))
        plt.legend()

        self._set_figure(fig, data_type)
        plt.close(fig)
