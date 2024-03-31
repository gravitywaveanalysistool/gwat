import customtkinter


class CustomGraphFrame(customtkinter.CTkToplevel):
    def __init__(self, master, gui, station, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.gui = gui
        self.button = None
        self.text_dialog = None
        self.x_selection = None
        self.y_selection = None
        self.fit_selection = None
        self.title("Custom Graph")

        # Set Icon
        self.iconbitmap("src/media/logo_notext_icon.ico")

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
            # print(f"{self.choose_bf.get()}, {self.x_selection}, {self.y_selection}")
            if self.choose_bf.get() and self.x_selection and self.y_selection is not None:
                self.gui.figs[f"{self.x_selection} vs. {self.y_selection}"] = graphs.graph2d(
                    pd.to_numeric(station.profile_df[self.x_selection]),
                    pd.to_numeric(station.profile_df[self.y_selection]),
                    int(self.choose_bf.get()),
                    self.x_selection,
                    self.y_selection,
                    f"{self.x_selection} vs. {self.y_selection}")

                self.gui.scrollable_frame.add_item(f"{self.x_selection} vs. {self.y_selection}")
                self.destroy()

        self.button = customtkinter.CTkButton(self, text="Create", command=create_graph)
        self.button.grid(row=6, column=0, padx=20, pady=10)

        self.lift()
        self.grab_set()