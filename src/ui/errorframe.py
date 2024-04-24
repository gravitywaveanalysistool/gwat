import customtkinter
from src.ui.hyperlinklabel import HyperlinkLabel

from src import datapath
from src.ui import windowicon


class ErrorFrame(customtkinter.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        """
        @param master:
        @param args:
        @param kwargs:
        """
        super().__init__(master, *args, **kwargs)
        self.button = None
        self.text_dialog = None

        # Set Icon
        windowicon.set_icon(self)

    def showerror(self, message, link=None):
        self.showdialog(message, link, "Error")

    def showdialog(self, message, link=None, title="Info"):
        """
        @param message: the body text of the dialog shown
        @param link:
        @param title: the title of the dialog shown
        @return:
        """
        self.title(title)

        if self.text_dialog:
            self.text_dialog.destroy()
        if self.button:
            self.button.destroy()

        self.text_dialog = customtkinter.CTkLabel(self, text=message, justify='left')
        self.text_dialog.grid(row=0, column=0, sticky="N", padx=20, pady=(20, 0))

        if link:
            link_text = link
            link_link = link
            if type(link) is tuple:
                link_text = link[0]
                link_link = link[1]
            link_label = HyperlinkLabel(self, text=link_text, link=link_link, justify='left')
            link_label.grid(row=1, column=0, padx=20, sticky='nw')

        def close_window():
            self.destroy()

        self.button = customtkinter.CTkButton(self, text="Ok", command=close_window)
        self.button.grid(row=2 if link else 1, column=0, padx=20, pady=10)

        self.lift()
        self.grab_set()

