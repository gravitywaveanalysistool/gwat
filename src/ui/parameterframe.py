import customtkinter


class ParameterFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, params, title, **kwargs):
        """
        @param master: 
        @param params:
        @param kwargs:
        """
        super().__init__(master, **kwargs)

        self.param_widgets = {}

        customtkinter.CTkLabel(self, text=title).grid(row=0, padx=(0, 10), pady=10, sticky="e")

        self.grid_columnconfigure(1, weight=1)

        self.set_params(params)

    def add_item(self, i, label, param):
        """
        @param i:
        @param label:
        @param param:
        @return:
        """
        label_widget = customtkinter.CTkLabel(self, text=label)
        param_widget = customtkinter.CTkLabel(self, text=param)

        label_widget.grid(row=i + 1, column=0, pady=(0, 10), padx=(0, 10), sticky="w")
        param_widget.grid(row=i + 1, column=1, pady=(0, 10), padx=(0, 10), sticky="e")

        self.param_widgets[label] = (label_widget, param_widget)

    def clear(self):
        for i, (_, (label_widget, param_widget)) in enumerate(self.param_widgets.items()):
            label_widget.destroy()
            param_widget.destroy()

    def set_params(self, params):
        self.clear()
        for i, (label, param) in enumerate(params.items()):
            self.add_item(i, label, param)
