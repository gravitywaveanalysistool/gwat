import customtkinter


class OptionsFrame(customtkinter.CTkToplevel):
    def __init__(self, master, options, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.options = options
        self.options_temp = self.options.copy()
        self.title("Options")

        # Create a global option list, maybe a dict. Persistent options in future? Cache Graphs?
        # Have some defaults
        # Gen graphs will pull from these options.
        # When an option changes, regenerate graphs
        # In the future, per graph options?

        def select_x(selection):
            self.x_selection = selection

        def select_y(selection):
            self.y_selection = selection

        # choose_poly_deg DropDown
        self.choose_poly_deg_lab = customtkinter.CTkLabel(self, text="Choose Poly Degree")
        self.choose_poly_deg_lab.grid(row=0, column=0, sticky="N", padx=20, pady=2)

        self.choose_poly_deg = customtkinter.CTkEntry(self)
        self.choose_poly_deg.grid(row=1, column=0, padx=20, pady=20)

        # Choose Y DropDown
        self.choose_ds_degree_lab = customtkinter.CTkLabel(self, text="Choose Data-Skip Degree")
        self.choose_ds_degree_lab.grid(row=2, column=0, sticky="N", padx=20, pady=2)

        self.choose_ds_degree = customtkinter.CTkEntry(self)
        self.choose_ds_degree.grid(row=3, column=0, padx=20, pady=20)

        def save():
            for key, value in self.options_temp.items():
                if key == 'degree':
                    self.options_temp[key] = self.choose_poly_deg.get()
                elif key == 'dataskip':
                    self.options_temp[key] = self.choose_ds_degree.get()

            options.update(self.options_temp)

            # Generate Graphs w/ new options

            self.destroy()

        def discard():
            self.destroy()

        self.save_button = customtkinter.CTkButton(self, text="Save", command=save)
        self.save_button.grid(row=4, column=0, padx=20, pady=10)

        self.discard_button = customtkinter.CTkButton(self, text="Discard", command=discard)
        self.discard_button.grid(row=5, column=0, padx=20, pady=10)

        self.lift()
        self.grab_set()