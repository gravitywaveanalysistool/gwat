import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphFrame(customtkinter.CTkFrame):
    def __init__(self, master=None, **kwargs):
        """
        @param master:
        @param kwargs:
        """
        super().__init__(master, **kwargs)

        self.canvas = None

    def draw_plot(self, fig):
        """
        @param fig:
        @return:
        """
        if self.canvas is not None:
            self.canvas.destroy()
        self.canvas = customtkinter.CTkCanvas(self)
        self.canvas.pack(fill='both', expand=1)
        self.canvas.fig_agg = FigureCanvasTkAgg(fig, master=self.canvas)
        self.canvas.fig_agg.draw()
        self.canvas.fig_agg.get_tk_widget().pack(fill='both', expand=1)
