import os.path
import unittest
import pandas as pd
import PyPDF2
from src import utils
from src.graphing.xygraph import XYGraph


def gen_graphs(count):
    data = pd.DataFrame({
        'Time': [1, 2, 3, 4, 5, 6, 7],
        'y0': [10, 30, 80, 70, 80, 40, 90],
        'y1': [20, 10, 50, 10, 80, 10, 80],
        'y2': [40, 40, 20, 50, 40, 80, 70],
        'y3': [50, 60, 40, 70, 30, 50, 60],
        'y4': [60, 80, 10, 90, 80, 30, 50],
        'y5': [80, 90, 00, 20, 30, 90, 20]
    })

    graph_objects = {}
    for i in range(0, min(count, 6)):
        graph_objects[str(i)] = XYGraph('Graph' + str(i), 'Time', 'y' + str(i), 2, 'X',
                                        'Y', False, False)

    for _, graph in graph_objects.items():
        graph.generate_graph(data, 'tropo')
        graph.generate_graph(data, 'strato')

    return graph_objects


class TestExportGraphs(unittest.TestCase):

    def export_test_impl(self, num_graphs, selected, expected_pages):
        graph_objects = gen_graphs(num_graphs)
        outfile = utils.get_temp_folder() + 'graphs.pdf'
        utils.save_graph_to_file(graph_objects, outfile, selected)

        def cleanup():
            if os.path.isfile(outfile):
                os.remove(outfile)

        self.addCleanup(cleanup)

        file_should_exist = expected_pages > 0
        self.assertEqual(os.path.isfile(outfile), file_should_exist)

        if file_should_exist:
            pdf = open(outfile, 'rb')
            pdf_reader = PyPDF2.PdfReader(outfile)
            self.assertEqual(expected_pages, len(pdf_reader.pages))
            pdf.close()

    def test_export_no_graphs(self):
        """
        Test to ensure utils.save_graph_to_file will not produce a file if no graphs objects are provided
        """
        self.export_test_impl(0, [], 0)

    def test_export_none_selected(self):
        """
        Test to ensure utils.save_graph_to_file will not produce a file if no graphs are selected
        """
        self.export_test_impl(1, [], 0)

    def test_export_no_graphs_1_selected(self):
        """
        Test to ensure utils.save_graph_to_file will not produce a file if graph objects are provided, even if a
        selection of graphs are provided
        """
        self.export_test_impl(0, ['0'], 0)

    def test_export_no_common_keys(self):
        """
        Test to ensure utils.save_graph_to_file will not produce a file if the selection does not select any graph
        objects
        """
        self.export_test_impl(1, ['invalid'], 0)

    def test_export_1_graph(self):
        """
        Test to ensure utils.save_graph_to_file will produce a file if at least one graph object is selected
        """
        self.export_test_impl(1, ['0'], 2)

    def test_export_4_selected(self):
        """
        Test to ensure utils.save_graph_to_file will produce a file with 2 pages per graph (strato, tropo)
        """
        self.export_test_impl(6, ['1', '3', '5', '4'], 8)


if __name__ == '__main__':
    unittest.main()
