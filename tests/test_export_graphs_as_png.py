import unittest
import os
from src.utils import save_graphs_as_png, get_temp_folder
from src.graphing.xygraph import XYGraph
import pandas as pd

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

# save_graphs_as_png(graph_objects, folder_path, selected_graphs)
class TestExportGraphsAsPng(unittest.TestCase):
    def export_test(self, num_graphs, selected_graphs, expected_pngs):
        directoryPath = get_temp_folder()
        graphFolderPath = directoryPath + "graphs"
        save_graphs_as_png(gen_graphs(num_graphs), directoryPath, selected_graphs)

        def cleanup():
            if os.path.isdir(graphFolderPath):
                for filename in os.listdir(graphFolderPath):
                    os.remove(graphFolderPath + "/" + filename)
                os.rmdir(graphFolderPath)

        self.addCleanup(cleanup)

        file_should_exist = expected_pngs > 0
        self.assertEqual(os.path.isdir(graphFolderPath), file_should_exist)

        if file_should_exist:
            graph_pngs = os.listdir(graphFolderPath)
            self.assertEqual(expected_pngs, len(graph_pngs))

    def test_no_graphs(self):
        self.export_test(0, [], 0)

    def test_no_selected_graphs(self):
        self.export_test(2, [], 0)

    def test_no_graphs_1_selected_graph(self):
        self.export_test(0, ['0'], 0)

    def test_key_mismatch(self):
        self.export_test(4, ['wacky key'], 0)

    def test_export_single_graph(self):
        self.export_test(1, ['0'], 2)

    def test_multiple_graphs(self):
        self.export_test(4, ['0','1','2'], 6)