from abc import ABC, abstractmethod


class Graph(ABC):
    def __init__(self, title, data):
        self.title = title
        self.data = data
        self.fig = None

    @abstractmethod
    def generate_graph(self):
        pass

    def get_figure(self):
        return self.fig
