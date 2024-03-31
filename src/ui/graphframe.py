import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphFrame(customtkinter.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.canvas = customtkinter.CTkCanvas(self)
        self.canvas.grid(row=0, column=0, padx=15, pady=15)

    def draw_plot(self, fig):
        self.canvas.delete('all')
        self.canvas.fig_agg = FigureCanvasTkAgg(fig, master=self.canvas)
        self.canvas.fig_agg.draw()
        self.canvas.fig_agg.get_tk_widget().pack(fill=customtkinter.BOTH, expand=True)