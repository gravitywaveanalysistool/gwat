import customtkinter as ctk


class ScrollingCheckButtonFrame(ctk.CTkFrame):
    def __init__(self, master, graph_objects, station, but_cmd=None, export_cmd=None, width=None, **kwargs):
        """
        @param master:
        @param graph_objects:
        @param station:
        @param but_cmd:
        @param export_cmd:
        @param width:
        @param kwargs:
        """
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.export_cmd = export_cmd

        self.all_selected = ctk.StringVar(value="off")
        self.select_all_checkbox = ctk.CTkCheckBox(self, text="Select All", width=10, variable=self.all_selected,
                                              onvalue='on', offvalue='off', command=self.select_all)
        self.select_all_checkbox.grid(row=0, column=0, pady=10, padx=10, sticky="e")

        export_graphs_button = ctk.CTkButton(self, text="Export Graphs", command=self.export)
        export_graphs_button.grid(row=0, column=1, pady=10, padx=(0, 10), sticky="ew")

        if width:
            self.scroll_frame = ctk.CTkScrollableFrame(self, width=width)
        else:
            self.scroll_frame = ctk.CTkScrollableFrame(self)

        self.scroll_frame.grid(row=1, column=0, pady=(10, 0), sticky="nsew", columnspan=2)

        self.scroll_frame.grid_columnconfigure(0, weight=1)
        self.scroll_frame.grid_columnconfigure(1, weight=2)
        self.scroll_frame.grid_columnconfigure(2, weight=2)

        self.graph_objects = graph_objects
        self.station = station

        self.but_cmd = but_cmd
        self.data_op_dict = {}
        self.button_list = []
        self.checkbox_dict = {}
        self.data_options = ['All', 'Stratosphere', 'Troposphere']
        for title, graph in graph_objects.items():
            self.add_item(title)

    def export(self):
        """
        @return:
        """
        selected_graphs = {}
        for name, (checkbox, graph_type) in self.checkbox_dict.items():
            print(name, graph_type)
            if checkbox.get():
                if graph_type == self.data_options[0]:
                    selected_graphs[name] = 'all'
                elif graph_type == self.data_options[1]:
                    selected_graphs[name] = 'strato'
                elif graph_type == self.data_options[2]:
                    selected_graphs[name] = 'tropo'
        self.export_cmd(selected_graphs)

    def select_all(self):
        """
        @return:
        """
        for _, (checkbox, _) in self.checkbox_dict.items():
            if self.all_selected.get() == 'on':
                checkbox.select()
            else:
                checkbox.deselect()

    def destroy(self):
        super().destroy()

    def add_item(self, title):
        """
        @param title:
        @return:
        """
        def select_graph_type(selection):
            self.checkbox_dict[title][1] = selection

        def check_cmd():
            if self.select_all_checkbox.get() == 'on':
                print('goof')
                self.select_all_checkbox.deselect()


        data_option = ctk.CTkOptionMenu(self.scroll_frame, values=self.data_options, command=select_graph_type)
        button = ctk.CTkButton(self.scroll_frame, text=title, width=100, height=24)
        checkbox = ctk.CTkCheckBox(self.scroll_frame, text="", width=10, command=check_cmd)
        if self.but_cmd is not None:
            button.configure(command=lambda: self.but_cmd(title))
        checkbox.grid(row=len(self.checkbox_dict), column=0, pady=(0, 10), sticky="e")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), sticky="w")
        data_option.grid(row=len(self.checkbox_dict), column=2, pady=(0, 10), sticky="e")

        self.data_op_dict[data_option] = title
        self.button_list.append(button)
        self.checkbox_dict[title] = (checkbox, self.data_options[0])

    def remove_item(self, item):
        """
        @param item:
        @return:
        """
        for button, checkbox in zip(self.button_list, self.checkbox_dict):
            if item == button.cget("text"):
                button.destroy()
                checkbox.destroy()

                self.button_list.remove(button)
                self.checkbox_dict.pop(item)
                return
