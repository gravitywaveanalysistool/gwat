from tkinter import filedialog

import customtkinter
import pandas as pd
from PIL import Image

from customgraphframe import CustomGraphFrame
from graphframe import GraphFrame
from optionsframe import OptionsFrame
from parameterframe import ParameterFrame
from scrollingbuttonframe import ScrollingCheckButtonFrame
from src import parseradfile
from src import utils
from src.graphing.hodograph import HodoGraph
from src.graphing.xygraph import XYGraph


class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # vars
        self.scrollable_frame = None
        self.checkbox_dict = None
        self.graph_frame = None
        self.param_frame = None
        self.station = None
        self.graph_objects = {}
        self.options = {'degree': '3', 'dataskip': '100'}

        self.title("Gravity Wave Analysis Tool")
        self.geometry("1200x800")

        # Allow upload button to expand anywhere
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Set Icon
        self.iconbitmap("src/media/logo_notext_icon.ico")

        def export_graphs():
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                     filetypes=(("PDF file", "*.pdf"), ("PNG files", "*.png")))

            if file_path:
                utils.save_graph_to_file(self.graph_objects, file_path, self.checkbox_dict, self)

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
            fig = self.graph_objects[title].get_figure()
            if self.graph_frame:
                self.graph_frame.destroy()
            self.graph_frame = GraphFrame(master=self)
            self.graph_frame.grid(row=0, column=1, padx=15, pady=15, rowspan=4, sticky="ne")
            self.graph_frame.draw_plot(fig)

        def generate_graphs(station):
            # Create initial Graph instances and select parameters
            self.graph_objects['Temperature Profile and Fit'] = XYGraph(title='Temperature Profile and Fit',
                                                                        data=station.profile_df,
                                                                        x='T',
                                                                        y='Alt',
                                                                        degree=6,
                                                                        x_label='Temperature (K)',
                                                                        y_label='Altitude (km)',
                                                                        best_fit=True)

            self.graph_objects['Wind Speed Profile and Fit'] = XYGraph(title='Wind Speed Profile and Fit',
                                                                       data=station.profile_df,
                                                                       x='Ws',
                                                                       y='Alt',
                                                                       degree=8,
                                                                       x_label='Wind Speed',
                                                                       y_label='Altitude',
                                                                       best_fit=True)

            self.graph_objects['Hodograph 1'] = HodoGraph(title='Hodograph 1',
                                                          data=station.profile_df,
                                                          comp_range=40,
                                                          line_width=5,
                                                          alt_threshold=200)

            self.graph_objects['Hodograph 2'] = HodoGraph(title='Hodograph 2',
                                                          data=station.profile_df,
                                                          comp_range=30,
                                                          line_width=1,
                                                          alt_threshold=200)

            # Generate their figures
            for _, graph in self.graph_objects.items():
                graph.generate_graph()

        def upload_file():
            file_path = filedialog.askopenfilename()

            if file_path:
                self.station = parseradfile.generate_profile_data(file_path)

                # GENERATE GRAPHS
                generate_graphs(self.station)

                # Delete Logo
                self.logo_label.destroy()

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
                self.scrollable_frame = ScrollingCheckButtonFrame(master=self, width=400,
                                                                  but_cmd=list_button_event,
                                                                  graph_objects=self.graph_objects,
                                                                  station=self.station)
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

        # Logo Display
        self.logo = customtkinter.CTkImage(light_image=Image.open("src/media/logo_text.png"),
                                           dark_image=Image.open("src/media/logo_text.png"),
                                           size=(600, 600))
        self.logo_label = customtkinter.CTkLabel(self, image=self.logo, text="")
        self.logo_label.grid(row=0, column=0, padx=15, pady=15)

        # Button for uploading file
        self.upload_button = customtkinter.CTkButton(self, text="Upload File", command=upload_file)
        self.upload_button.grid(row=1, column=0, padx=15, pady=15, sticky="n")


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("src/ui/orange_theme.json")
    app = GUI()
    app.mainloop()
