from tkinter import filedialog

import pandas as pd
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src import graphs
from src import utils
from src import parseradfile
from graphframe import GraphFrame
from scrollingbuttonframe import ScrollingCheckButtonFrame
from parameterframe import ParameterFrame
from customgraphframe import CustomGraphFrame
from optionsframe import OptionsFrame
from errorframe import ErrorFrame


class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # vars
        self.scrollable_frame = None
        self.checkbox_dict = None
        self.graph_frame = None
        self.param_frame = None
        self.station = None
        self.figs = {}
        self.options = {'degree': '3', 'dataskip': '100'}

        self.title("Gravity Wave Analysis Tool")
        self.geometry("1200x800")

        # Allow upload button to expand anywhere
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        def export_graphs():
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                     filetypes=(("PDF file", "*.pdf"), ("PNG files", "*.png")))

            if file_path:
                utils.save_graph_to_file(self.figs, file_path, self.checkbox_dict, self)

        def export_params():
            file = filedialog.asksaveasfile(defaultextension=".txt")
            if file:
                for i, (label, param) in enumerate(self.param_frame.params.items()):
                    file.write(label + ',' + param + '\n')

        def create_custom_graph():
            CustomGraphFrame(self, self, self.station)

        def show_options():
            OptionsFrame(self, self.options)

        def list_button_event(title):
            fig = self.figs[title]
            if self.graph_frame:
                self.graph_frame.destroy()
            self.graph_frame = GraphFrame(master=self)
            self.graph_frame.grid(row=0, column=1, padx=15, pady=15, rowspan=4, sticky="ne")
            self.graph_frame.draw_plot(fig)

        def generate_graphs(station):
            # Create a list of graph figures from the station list
            self.figs['Temperature Profile and Fit'] = (graphs.graph2d((pd.to_numeric(station.profile_df['T']) + 273),
                                                                       (pd.to_numeric(
                                                                           station.profile_df['Alt']) / 1000),
                                                                       6,
                                                                       'Temperature (K)',
                                                                       'Altitude (km)',
                                                                       'Temperature Profile and Fit'))

            self.figs['Wind Speed Profile and Fit'] = graphs.graph2d(pd.to_numeric(station.profile_df['Ws']),
                                                                     pd.to_numeric(station.profile_df['Alt']),
                                                                     8,
                                                                     'Wind Speed',
                                                                     'Altitude',
                                                                     'Wind Speed Profile and Fit')
            self.figs['Hodograph 1'] = graphs.hodograph(40, 2, station.profile_df)
            self.figs['Hodograph 2'] = graphs.hodograph(30, 1, station.profile_df)

        def upload_file():
            file_path = filedialog.askopenfilename()

            if file_path:
                self.station = parseradfile.generate_profile_data(file_path)

                # GENERATE GRAPHS
                generate_graphs(self.station)

                # Make upload button not expand and move to top
                self.upload_button.grid(row=1, column=0, padx=15, pady=15)
                self.grid_columnconfigure(0, weight=0)
                self.grid_rowconfigure(0, weight=0)

                # Make Options button not expand
                self.grid_rowconfigure(1, weight=0)

                # Make Custom button not expand
                self.grid_rowconfigure(2, weight=0)

                # Allow scroll frame to expand
                self.grid_rowconfigure(3, weight=1)

                # Make Export Graph button not expand
                self.grid_rowconfigure(4, weight=0)

                # Create Options Button
                self.options_button = customtkinter.CTkButton(self, text="Options", command=show_options)
                self.options_button.grid(row=0, column=0, padx=15, pady=15)

                # Create Custom Graph Button
                self.upload_button = customtkinter.CTkButton(self, text="Custom Graph", command=create_custom_graph)
                self.upload_button.grid(row=2, column=0, padx=15, pady=15)

                # Create scrollable checkbox frame
                self.scrollable_frame = ScrollingCheckButtonFrame(master=self, width=300,
                                                                  but_cmd=list_button_event,
                                                                  figs=self.figs)
                self.scrollable_frame.grid(row=3, column=0, padx=15, pady=15, rowspan=2, sticky="nsew")
                self.checkbox_dict = self.scrollable_frame.checkbox_dict

                # Create Export Graph Button
                self.upload_button = customtkinter.CTkButton(self, text="Export Graph(s)", command=export_graphs)
                self.upload_button.grid(row=5, column=0, padx=15, pady=15)

                # Create Export Params Button
                self.upload_button = customtkinter.CTkButton(self, text="Export Params", command=export_params)
                self.upload_button.grid(row=5, column=1, padx=15, pady=15)

                # Create Param Frame
                params = {}
                for i in range(10):
                    params[f"Param {i}"] = f"value {i}"

                self.param_frame = ParameterFrame(master=self, params=params, width=600)
                self.param_frame.grid(row=3, column=1, padx=15, pady=15, sticky="sew")
                # self.grid_rowconfigure((1, 3), weight=0)

        # Button for uploading file
        self.upload_button = customtkinter.CTkButton(self, text="Upload File", command=upload_file)
        self.upload_button.grid(row=0, column=0, padx=15, pady=15)


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = GUI()
    app.mainloop()
