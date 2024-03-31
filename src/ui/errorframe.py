import customtkinter


class ErrorFrame(customtkinter.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.button = None
        self.text_dialog = None
        self.title("Error")

    def showerror(self, message):
        if self.text_dialog:
            self.text_dialog.destroy()
        if self.button:
            self.button.destroy()

        self.text_dialog = customtkinter.CTkLabel(self, text=message)
        self.text_dialog.grid(row=0, column=0, sticky="N", padx=20, pady=20)

        def close_window():
            self.destroy()

        self.button = customtkinter.CTkButton(self, text="Ok", command=close_window)
        self.button.grid(row=1, column=0, padx=20, pady=10)

        self.update_geometry()
        self.lift()
        self.grab_set()

    def update_geometry(self):
        self.update_idletasks()
        width = self.winfo_reqwidth() + 20
        height = self.winfo_reqheight() + 20
        self.geometry(f"{width}x{height}")