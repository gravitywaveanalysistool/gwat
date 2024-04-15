import unittest
import numpy as np
from matplotlib.figure import Figure

from src.graphing.xygraph import XYGraph
from src.graphing.graph import Graph


class TestXYGraph(unittest.TestCase):
    def test_xygraph(self):
        test_graph = XYGraph(
            title="Test Graph",
            x="x",
            y="y",
            degree=2,
            x_label="X",
            y_label="Y",
            best_fit=True,
            draw_lines=True
        )
        self.assertIsNotNone(test_graph)
        self.assertIsInstance(test_graph, Graph)

        self.assertIsNotNone(test_graph.title)
        self.assertIsNotNone(test_graph.x)
        self.assertIsNotNone(test_graph.y)
        self.assertIsNotNone(test_graph.degree)
        self.assertIsNotNone(test_graph.x_label)
        self.assertIsNotNone(test_graph.y_label)
        self.assertIsNotNone(test_graph.best_fit)
        self.assertIsNotNone(test_graph.draw_lines)

    def test_generate_graph(self):
        # Dummy data
        data = {
            'x': np.array([1, 2, 3, 4, 5]),
            'y': np.array([2, 4, 6, 8, 10])
        }

        test_graph = XYGraph(
            title="Test Graph",
            x="x",
            y="y",
            degree=2,
            x_label="X",
            y_label="Y",
            best_fit=True,
            draw_lines=True
        )

        test_graph.generate_graph(data, "tropo")
        test_graph.generate_graph(data, "strato")

        self.assertIsNotNone(test_graph.tropo_fig)
        self.assertIsInstance(test_graph.tropo_fig, Figure)
        self.assertIsNotNone(test_graph.strato_fig)
        self.assertIsInstance(test_graph.strato_fig, Figure)


if __name__ == '__main__':
    unittest.main()
