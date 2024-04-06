from abc import ABC, abstractmethod


class Graph(ABC):
    def __init__(self, title):
        """
        Set's default properties upon instantiation

        @param title: string
        """
        self.title = title
        self.strato_fig = None
        self.tropo_fig = None

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
        else:
            self.tropo_fig = fig

    def _graph_title(self, data_type):
        if data_type == 'strato':
            return self.title + ' (Stratosphere)'
        else:
            return self.title + ' (Troposphere)'

    def get_figure(self, data_type):
        """
        Gets the corresponding figure for the given data type

        @param data_type: "strato" | "tropo"
        @return: strato_fig | tropo_fig : matplotlib figure
        """
        if data_type == "strato":
            return self.strato_fig
        else:
            return self.tropo_fig
