import numpy as np
from matplotlib import pyplot as plt
from metpy.plots import Hodograph
from matplotlib.cm import get_cmap
from src.graphing.graph import Graph


class HodoGraph(Graph):
    def __init__(self, title, data, comp_range, line_width, alt_threshold):
        super().__init__(title, data)
        self.comp_range = comp_range
        self.line_width = line_width
        self.alt_threshold = alt_threshold

    def generate_graph(self):
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(1, 1, 1)
        hodo = Hodograph(ax, component_range=self.comp_range)
        hodo.add_grid(increment=10)
        hodo.add_grid(increment=20, linestyle='-')

        cmap = get_cmap('viridis')
        norm = plt.Normalize(vmin=self.data['Alt'].min(), vmax=self.data['Alt'].max())

        # plot the points and color them every 300m
        last_alt = self.data['Alt'].iloc[0] - self.alt_threshold
        for i in range(len(self.data['U']) - 1):
            if self.data['Alt'].iloc[i] >= last_alt + self.alt_threshold:
                segment_color = cmap(norm(self.data['Alt'].iloc[i]))
                hodo.plot(self.data['U'][i:i + 2], self.data['V'][i:i + 2], color=segment_color, linewidth=self.line_width,
                          label=f'{self.data["Alt"].iloc[i]:.0f}-{self.data["Alt"].iloc[i + 1]:.0f} m')
                last_alt = self.data['Alt'].iloc[i]

        # axis names and alt bar
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cb = fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
        cb.set_label('Altitude (m)')
        ax.set_xlabel('U Component (m/s)')
        ax.set_ylabel('V Component (m/s)')

        self.fig = fig
