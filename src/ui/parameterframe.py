import customtkinter


class ParameterFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, params, **kwargs):
        """
        @param master: 
        @param params:
        @param kwargs:
        """
        super().__init__(master, **kwargs)

        self.params = params

        for i, (label, param) in enumerate(params.items()):
            self.add_item(i, label, param)

    def add_item(self, i, label, param):
        """
        @param i:
        @param label:
        @param param:
        @return:
        """
        label = customtkinter.CTkLabel(self, text=label)
        param = customtkinter.CTkLabel(self, text=param)

        label.grid(row=i, column=0, pady=(0, 10), padx=(0, 10), sticky="w")
        param.grid(row=i, column=1, pady=(0, 10), padx=(0, 10), sticky="e")