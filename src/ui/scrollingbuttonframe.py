import customtkinter


class ScrollingCheckButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, graph_objects, station, but_cmd=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=2)

        self.graph_objects = graph_objects
        self.station = station

        self.but_cmd = but_cmd
        self.radiobutton_variable = customtkinter.StringVar()
        self.data_op_dict = {}
        self.button_list = []
        self.checkbox_dict = {}
        self.data_options = ['All', 'Stratosphere', 'Troposphere']
        for title, graph in graph_objects.items():
            self.add_item(title)

    def destroy(self):
        super().destroy()
        self._parent_frame.destroy()

    def add_item(self, title):
        def option_event(selection):
            print(selection)
            if selection == 'Stratosphere':
                self.graph_objects[title].data = self.station.strato_df
            if selection == 'Troposphere':
                self.graph_objects[title].data = self.station.tropo_df
            if selection == 'All':
                self.graph_objects[title].data = self.station.profile_df
            self.graph_objects[title].generate_graph()

        data_option = customtkinter.CTkOptionMenu(self, values=self.data_options, command=option_event)
        button = customtkinter.CTkButton(self, text=title, width=100, height=24)
        checkbox = customtkinter.CTkCheckBox(self, text="", width=10)
        if self.but_cmd is not None:
            button.configure(command=lambda: self.but_cmd(title))
        checkbox.grid(row=len(self.checkbox_dict), column=0, pady=(0, 10), sticky="e")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), sticky="w")
        data_option.grid(row=len(self.checkbox_dict), column=2, pady=(0, 10), sticky="e")

        self.data_op_dict[data_option] = title
        self.button_list.append(button)
        self.checkbox_dict[title] = checkbox

    def remove_item(self, item):
        for button, checkbox in zip(self.button_list, self.checkbox_dict):
            if item == button.cget("text"):
                button.destroy()
                checkbox.destroy()

                self.button_list.remove(button)
                self.checkbox_dict.pop(item)
                return