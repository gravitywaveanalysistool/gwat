import unittest
import numpy as np
import pandas as pd
from matplotlib.figure import Figure

from src.graphing.hodograph import HodoGraph
from src.graphing.graph import Graph


class TestXYGraph(unittest.TestCase):
    def test_hodograph(self):
        test_graph = HodoGraph(
            title="Test Graph",
            comp_range=40,
            line_width=2,
            alt_threshold=100
        )

        self.assertIsNotNone(test_graph)
        self.assertIsInstance(test_graph, Graph)

        self.assertIsNotNone(test_graph.title)
        self.assertIsNotNone(test_graph.comp_range)
        self.assertIsNotNone(test_graph.line_width)
        self.assertIsNotNone(test_graph.alt_threshold)


    def test_generate_graph(self):
        # Dummy data
        data = {
            'Alt': np.array([1, 2, 3, 4, 5]),
            'UP': np.array([2, 4, 6, 8, 10]),
            'VP': np.array([2, 4, 6, 8, 10])
        }

        df = pd.DataFrame(data)

        test_graph = HodoGraph(
            title="Test Graph",
            comp_range=40,
            line_width=2,
            alt_threshold=100
        )

        test_graph.generate_graph(df, "tropo")
        test_graph.generate_graph(df, "strato")

        self.assertIsNotNone(test_graph.tropo_fig)
        self.assertIsInstance(test_graph.tropo_fig, Figure)
        self.assertIsNotNone(test_graph.strato_fig)
        self.assertIsInstance(test_graph.strato_fig, Figure)


if __name__ == '__main__':
    unittest.main()
