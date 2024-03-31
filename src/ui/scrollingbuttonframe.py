import customtkinter


class ScrollingCheckButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, figs, but_cmd=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        self.but_cmd = but_cmd
        self.radiobutton_variable = customtkinter.StringVar()
        self.button_list = []
        self.checkbox_dict = {}
        for title, fig in figs.items():
            self.add_item(title)

    def add_item(self, item):
        button = customtkinter.CTkButton(self, text=item, width=100, height=24)
        checkbox = customtkinter.CTkCheckBox(self, text="", width=10)
        if self.but_cmd is not None:
            button.configure(command=lambda: self.but_cmd(item))
        checkbox.grid(row=len(self.checkbox_dict), column=0, pady=(0, 10), sticky="e")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), sticky="w")

        self.button_list.append(button)
        self.checkbox_dict[item] = checkbox

    def remove_item(self, item):
        for button, checkbox in zip(self.button_list, self.checkbox_dict):
            if item == button.cget("text"):
                button.destroy()
                checkbox.destroy()

                self.button_list.remove(button)
                self.checkbox_dict.pop(item)
                return