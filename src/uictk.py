from tkinter import filedialog

import pandas as pd
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import test
import graphs


class ScrollingCheckButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, figs, check_cmd=None, but_cmd=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        self.check_cmd = check_cmd
        self.but_cmd = but_cmd
        self.radiobutton_variable = customtkinter.StringVar()
        self.button_list = []
        self.checkbox_list = []
        for title, fig in figs.items():
            self.add_item(title)  # Add the title to your UI

    def add_item(self, item):
        button = customtkinter.CTkButton(self, text=item, width=100, height=24)
        checkbox = customtkinter.CTkCheckBox(self, text="", width=10)
        if self.but_cmd and self.check_cmd is not None:
            button.configure(command=lambda: self.but_cmd(item))
            checkbox.configure(command=self.check_cmd)
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10), sticky="e")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), sticky="w")

        self.button_list.append(button)
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for button, checkbox in zip(self.button_list, self.checkbox_list):
            if item == button.cget("text"):
                button.destroy()
                checkbox.destroy()

                self.button_list.remove(button)
                self.checkbox_list.remove(checkbox)
                return


class GraphFrame(customtkinter.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Create a canvas to display the plot
        self.canvas = customtkinter.CTkCanvas(self)
        self.canvas.grid(row=0, column=0, padx=15, pady=15)

    def draw_plot(self, fig):
        self.canvas.fig_agg = FigureCanvasTkAgg(fig, master=self.canvas)
        self.canvas.fig_agg.draw()
        self.canvas.fig_agg.get_tk_widget().pack(fill=customtkinter.BOTH, expand=True)


class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # vars
        file_path = None
        figs = {}

        self.title("Gravity Wave Analysis Tool")
        self.geometry("1200x800")

        # Allow upload button to expand anywhere
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        def export_graphs():
            raise NotImplementedError("Scott")

        def create_custom_graph():
            raise NotImplementedError("Subclasses must implement configure_layout method")

        def list_checkmark_event():
            pass

        def list_button_event(title):
            fig = figs[title]
            self.graph_frame = GraphFrame(master=self)
            self.graph_frame.grid(row=0, column=1, padx=15, pady=15, rowspan=3, sticky="ne")
            self.graph_frame.draw_plot(fig)

        def generate_graphs(station):
            # Create a list of graph figures from the station list
            figs['Temperature Profile and Fit'] = (graphs.graph2d((pd.to_numeric(station.profile_df['T']) + 273),
                                                                  (pd.to_numeric(station.profile_df['Alt']) / 1000),
                                                                  6,
                                                                  'Temperature (K)',
                                                                  'Altitude (km)',
                                                                  'Temperature Profile and Fit'))

            figs['Wind Speed Profile and Fit'] = graphs.graph2d(pd.to_numeric(station.profile_df['Ws']),
                                                                pd.to_numeric(station.profile_df['Alt']),
                                                                8,
                                                                'Wind Speed',
                                                                'Altitude',
                                                                'Wind Speed Profile and Fit')
            # figs['Hodograph 1'] = graphs.hodograph(40, 2, station.profile_df)
            # figs['Hodograph 2'] = graphs.hodograph(30, 1, station.profile_df)

        def upload_file():
            nonlocal file_path
            file_path = filedialog.askopenfilename()

            if file_path:
                station = test.generate_profile_data(file_path)

                # GENERATE GRAPHS
                generate_graphs(station)

                # Make upload button not expand
                self.grid_columnconfigure(0, weight=0)
                self.grid_rowconfigure(0, weight=0)

                # Make Custom button not expand
                self.grid_rowconfigure(1, weight=0)

                # Make Export button not expand
                self.grid_rowconfigure(3, weight=0)

                # Allow scroll frame to expand
                self.grid_rowconfigure(2, weight=1)

                # Create scrollable checkbox frame
                self.scrollable_frame = ScrollingCheckButtonFrame(master=self, width=300,
                                                                  check_cmd=list_checkmark_event,
                                                                  but_cmd=list_button_event,
                                                                  figs=figs)
                self.scrollable_frame.grid(row=2, column=0, padx=15, pady=15, sticky="nsew")

                # Create Custom Graph Button
                self.upload_button = customtkinter.CTkButton(self, text="Custom Graph", command=create_custom_graph)
                self.upload_button.grid(row=1, column=0, padx=15, pady=15)

                # Create Export Graph Button
                self.upload_button = customtkinter.CTkButton(self, text="Export Graph(s)", command=export_graphs)
                self.upload_button.grid(row=3, column=0, padx=15, pady=15)

        # Button for uploading file
        self.upload_button = customtkinter.CTkButton(self, text="Upload File", command=upload_file)
        self.upload_button.grid(row=0, column=0, padx=15, pady=15)


def main():
    customtkinter.set_appearance_mode("dark")
    app = GUI()
    app.mainloop()