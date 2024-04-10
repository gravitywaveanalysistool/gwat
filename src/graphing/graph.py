from abc import ABC, abstractmethod

import copy


class Graph(ABC):
    def __init__(self, title):
        """
        Set's default properties upon instantiation

        @param title: string
        """
        self.title = title
        self.strato_fig = None
        self.tropo_fig = None
        self.export_strato_fig = None
        self.export_tropo_fig = None

    @abstractmethod
    def generate_graph(self, data, data_type):
        pass

    def _set_figure(self, fig, data_type):
        """
        Sets the figure to the corresponding figure for the given data type

        @param fig:
        @param data_type:
        @return:
        """
        if data_type == "strato":
            self.strato_fig = fig
            self.export_strato_fig = copy.deepcopy(fig)
        else:
            self.tropo_fig = fig
            self.export_tropo_fig = copy.deepcopy(fig)

    def _graph_title(self, data_type):
        if data_type == 'strato':
            return self.title + ' (Stratosphere)'
        else:
            return self.title + ' (Troposphere)'

    def get_figure(self, data_type, export=False):
        """
        Gets the corresponding figure for the given data type

        @param data_type: "strato" | "tropo"
        @return: strato_fig | tropo_fig : matplotlib figure
        """
        if data_type == "strato":
            return self.export_strato_fig if export else self.strato_fig
        else:
            return self.export_tropo_fig if export else self.tropo_fig
