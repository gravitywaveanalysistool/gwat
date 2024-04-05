import customtkinter
import pandas as pd

from src import datapath
from src.graphing.hodograph import HodoGraph
from src.graphing.xygraph import XYGraph

class CustomGraphFrame(customtkinter.CTkToplevel):
    def __init__(self, master, gui, station, *args, **kwargs):
        """
        @param master:
        @param gui:
        @param station:
        @param args:
        @param kwargs:
        """
        super().__init__(master, *args, **kwargs)
        self.gui = gui
        self.button = None
        self.text_dialog = None
        self.x_selection = None
        self.y_selection = None
        self.fit_selection = None
        self.title("Custom Graph")

        # Set Icon
        self.iconbitmap(datapath.getDataPath("media/logo_notext_icon.ico"))

        def select_x(selection):
            self.x_selection = selection

        def select_y(selection):
            self.y_selection = selection

        # Convert labels to a list
        label_list = station.profile_df.columns.tolist()

        # Create Default Values
        self.x_selection = label_list[0]
        self.y_selection = label_list[0]

        # Choose X DropDown
        self.x_label = customtkinter.CTkLabel(self, text="Choose X-Axis")
        self.x_label.grid(row=0, column=0, sticky="N", padx=20, pady=2)

        self.choose_x = customtkinter.CTkOptionMenu(self, values=label_list, command=select_x)
        self.choose_x.grid(row=1, column=0, padx=20, pady=20)

        # Choose Y DropDown
        self.y_label = customtkinter.CTkLabel(self, text="Choose Y-Axis")
        self.y_label.grid(row=2, column=0, sticky="N", padx=20, pady=2)

        self.choose_y = customtkinter.CTkOptionMenu(self, values=label_list, command=select_y)
        self.choose_y.grid(row=3, column=0, padx=20, pady=20)

        # Choose best fit degree
        self.fit_label = customtkinter.CTkLabel(self, text="Choose Fit Degree")
        self.fit_label.grid(row=4, column=0, sticky="N", padx=20, pady=2)

        self.choose_bf = customtkinter.CTkEntry(self)
        self.choose_bf.grid(row=5, column=0, padx=20, pady=20)

        def create_graph():
            """
            @return:
            """
            if self.choose_bf.get() and self.x_selection and self.y_selection is not None:
                title = f"{self.x_selection} vs. {self.y_selection}"

                # Create graph instance
                self.gui.graph_objects[title] = XYGraph(
                    title=title,
                    data=station.profile_df,
                    x=self.x_selection,
                    y=self.y_selection,
                    degree=int(self.choose_bf.get()),
                    x_label=self.x_selection,
                    y_label=self.y_selection,
                    best_fit=True)

                # Generate its figure
                self.gui.graph_objects[title].generate_graph()

                self.gui.scrollable_frame.add_item(title)
                self.destroy()

        self.button = customtkinter.CTkButton(self, text="Create", command=create_graph)
        self.button.grid(row=6, column=0, padx=20, pady=10)

        self.lift()
        self.grab_set()