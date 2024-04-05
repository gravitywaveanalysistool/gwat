from abc import ABC, abstractmethod


class Graph(ABC):
    def __init__(self, title):
        self.title = title
        self.strato_fig = None
        self.tropo_fig = None

    @abstractmethod
    def generate_graph(self, data, data_type):
        pass

    def _set_figure(self, fig, data_type):
        if data_type == "strato":
            self.strato_fig = fig
        else:
            self.tropo_fig = fig

    def get_figure(self, data_type):
        if data_type == "strato":
            return self.strato_fig
        else:
            return self.tropo_fig
