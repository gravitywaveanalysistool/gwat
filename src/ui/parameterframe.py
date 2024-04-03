import customtkinter


class ParameterFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, params, **kwargs):
        super().__init__(master, **kwargs)

        self.params = params

        for i, (label, param) in enumerate(params.items()):
            self.add_item(i, label, param)

    def add_item(self, i, label, param):
        label = customtkinter.CTkLabel(self, text=label)
        param = customtkinter.CTkLabel(self, text=param)

        label.grid(row=i, column=0, pady=(0, 10), padx=(0, 10), sticky="w")
        param.grid(row=i, column=1, pady=(0, 10), padx=(0, 10), sticky="e")