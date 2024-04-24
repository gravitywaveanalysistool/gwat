import customtkinter as ctk
import webbrowser


class HyperlinkLabel(ctk.CTkLabel):
    def __init__(self, master, text, link, **kwargs):
        super().__init__(master, text=text, text_color='#77aaff', cursor='hand2', font=ctk.CTkFont(underline=True),
                         **kwargs)
        self.bind('<Button 1>', lambda _: webbrowser.open(link))
