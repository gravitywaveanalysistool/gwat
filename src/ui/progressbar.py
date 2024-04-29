import tkinter
from tkinter import ttk

import customtkinter as ctk


class ProgressBar(ctk.CTkToplevel):
    def __init__(self, master, label, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.resizable(False, False)
        self.title("Progress")

        self.label = ctk.CTkLabel(self, text=label)
        self.label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.progressbar = ctk.CTkProgressBar(self, orientation=ctk.HORIZONTAL, mode='indeterminate', height=20)
        self.progressbar.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.lift()
        self.grab_set()

    def start_bar(self):
        self.progressbar.start()

    def stop_bar(self):
        self.progressbar.stop()
        self.destroy()

    # def update_bar(self, value):
    #     print(self.progressbar.get())
    #     self.progressbar.set(value)
    #
    #     #if value > 1.0:
    #     #    self.destroy()

    # def change_label(self, label):
    #     self.label.configure(text=label)
