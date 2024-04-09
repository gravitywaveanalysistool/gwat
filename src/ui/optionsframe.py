import customtkinter

from src import datapath
from src.utils import save_options
from src.graphing.hodograph import HodoGraph
from src.graphing.xygraph import XYGraph


class OptionsFrame(customtkinter.CTkToplevel):
    def __init__(self, master, graph_objects, station, options, *args, **kwargs):
        """
        @param master:
        @param options:
        @param args:
        @param kwargs:
        """
        super().__init__(master, *args, **kwargs)
        self.graph_objects = graph_objects
        self.graph_list = list(graph_objects.keys())
        self.theme_list = ["Dark", "Colorblind"]
        self.graph_selection = self.graph_list[0]
        self.station = station
        self.options = options
        self.options_temp = self.options.copy()
        self.title("Options")

        # TODO find better way than this
        self.ch_poly_deg_entry = None
        self.ch_ds_degree_entry = None
        self.theme_selection = 'Dark'

        # Set Icon
        # self.iconbitmap(".." + datapath.getDataPath("media/logo_notext_icon.ico"))

        # Graph Option Container
        self.graph_op_cont = customtkinter.CTkFrame(self)

        def clear_entries():
            if self.ch_poly_deg_entry is not None:
                self.ch_poly_deg_entry.destroy()
            if self.ch_ds_degree_entry is not None:
                self.ch_ds_degree_entry.destroy()

        def select_graph_event(selection):
            self.graph_selection = selection

            if isinstance(graph_objects[self.graph_selection], XYGraph):
                clear_entries()

                # Select Poly Deg. Entry
                self.ch_poly_deg_lab = customtkinter.CTkLabel(self.graph_op_cont, text="Choose Poly Degree")
                self.ch_poly_deg_lab.grid(row=2, column=0, sticky="N", padx=10, pady=10)

                self.ch_poly_deg_entry = customtkinter.CTkEntry(self.graph_op_cont)
                self.ch_poly_deg_entry.grid(row=3, column=0, padx=10, pady=(0, 10))

            elif isinstance(graph_objects[self.graph_selection], HodoGraph):
                clear_entries()

                # Select Data Skip Entry
                self.ch_ds_degree_lab = customtkinter.CTkLabel(self.graph_op_cont, text="Choose Data-Skip Degree")
                self.ch_ds_degree_lab.grid(row=2, column=0, sticky="N", padx=10, pady=10)

                self.ch_ds_degree_entry = customtkinter.CTkEntry(self.graph_op_cont)
                self.ch_ds_degree_entry.grid(row=3, column=0, padx=10, pady=(0, 10))

        # Choose Graph Drop Down
        self.ch_graph_label = customtkinter.CTkLabel(self.graph_op_cont, text="Choose Graph")
        self.ch_graph_label.grid(row=0, column=0, sticky="N", padx=10, pady=10)

        self.ch_graph_drop = customtkinter.CTkOptionMenu(self.graph_op_cont, values=self.graph_list, command=select_graph_event)
        self.ch_graph_drop.set(self.graph_list[0])
        select_graph_event(self.graph_list[0])
        self.ch_graph_drop.grid(row=1, column=0, padx=10, pady=(0, 10))

        self.graph_op_cont.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # def select_theme(selection):
        #     self.theme_selection = selection
        #
        # # Choose Colorblind mode dropdown (std, deuteranopia, protanopia, tritanopia)
        # self.ch_dis_mode_label = customtkinter.CTkLabel(self, text="Choose Display Mode")
        # self.ch_dis_mode_label.grid(row=4, column=0, sticky="N", padx=20, pady=2)
        #
        # self.ch_dis_mode_drop = customtkinter.CTkOptionMenu(self, values=self.theme_list, command=select_theme)
        # self.ch_dis_mode_drop.grid(row=5, column=0, padx=20, pady=20)

        def save():
            """
            @return:
            """
            if isinstance(graph_objects[self.graph_selection], XYGraph) and self.ch_poly_deg_entry is not None:
                graph_objects[self.graph_selection].degree = int(self.ch_poly_deg_entry.get())
                update_graph()

            elif isinstance(graph_objects[self.graph_selection], HodoGraph) and self.ch_ds_degree_entry is not None:
                graph_objects[self.graph_selection].alt_threshold = int(self.ch_ds_degree_entry.get())
                update_graph()

            # if self.theme_selection == 'Dark':
            #     print("huh")
            #     customtkinter.set_default_color_theme(datapath.getDataPath("orange_theme.json"))
            # elif self.theme_selection == 'Colorblind':
            #     print("huh^2")
            #     customtkinter.set_default_color_theme(datapath.getDataPath("color_blind_friendly_theme.json"))

            # options.update(self.options_temp)
            # save_options(self.options)

            self.destroy()

        def update_graph():
            self.graph_objects[self.graph_selection].generate_graph(self.station.strato_df, "strato")
            self.graph_objects[self.graph_selection].generate_graph(self.station.tropo_df, "tropo")

        def discard():
            """
            @return:
            """
            self.destroy()

        self.save_button = customtkinter.CTkButton(self, text="Save", command=save, width=50)
        self.save_button.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

        self.discard_button = customtkinter.CTkButton(self, text="Discard", command=discard, width=50)
        self.discard_button.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.lift()
        self.grab_set()
