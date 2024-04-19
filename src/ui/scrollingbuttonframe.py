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
        self.selected_button = None
        self.checkbox_dict = {}
        for title, graph in graph_objects.items():
            self.add_item(title)

    def export(self):
        """
        @return:
        """
        selected_graphs = []
        for name, checkbox in self.checkbox_dict.items():
            if checkbox.get():
                selected_graphs.append(name)

        self.export_cmd(selected_graphs)

    def select_all(self):
        """
        @return:
        """
        for _, checkbox in self.checkbox_dict.items():
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

        def check_cmd():
            if self.select_all_checkbox.get() == 'on':
                self.select_all_checkbox.deselect()

        button = ctk.CTkButton(self.scroll_frame, text=title, anchor="w")
        checkbox = ctk.CTkCheckBox(self.scroll_frame, text="", width=10, command=check_cmd)

        checkbox.grid(row=len(self.checkbox_dict), column=0, pady=(0, 10), sticky="e")

        def button_select():
            self.but_cmd(title)
            self.select_button(button)

        if self.but_cmd is not None:
            button.configure(command=button_select)
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), sticky="we")

        if len(self.button_list) == 0:
            self.select_button(button)

        self.button_list.append(button)
        self.checkbox_dict[title] = checkbox

    def select_button(self, button):
        if self.selected_button is not None:
            default_fg_color = button.cget('fg_color')
            default_text_color = button.cget('text_color')
            default_hover_color = button.cget('hover_color')
            self.selected_button.configure(fg_color=default_fg_color, text_color=default_text_color,
                                           hover_color=default_hover_color)

        self.selected_button = button
        button.configure(fg_color='white', text_color='black', hover_color='#bbbbbb')
