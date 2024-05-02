import customtkinter as ctk
from customtkinter.windows.widgets.scaling import ScalingTracker
import json
from PIL import Image

from src.ui.hyperlinklabel import HyperlinkLabel
from src import datapath


class AuthorCard(ctk.CTkFrame):
    def __init__(self, master, name, email, linkedin, github, photo, **kwargs):
        super().__init__(master, fg_color='gray20', **kwargs)
        self.grid_columnconfigure(0, weight=1)

        (ctk.CTkLabel(self, image=ctk.CTkImage(Image.open(photo), size=(120, 120)), text='')
         .grid(row=0, column=0, sticky='nsew', padx=10, pady=10, ))

        (ctk.CTkLabel(self, text=name, font=ctk.CTkFont(size=18), justify='left')
         .grid(row=1, column=0, sticky='w', padx=10))

        (HyperlinkLabel(self, text=email, link='mailto:' + email, justify='left')
         .grid(row=2, column=0, sticky='w', padx=10))

        (HyperlinkLabel(self, text='GitHub', link=github, justify='left')
         .grid(row=3, column=0, sticky='w', padx=10))

        if linkedin is not None:
            (HyperlinkLabel(self, text='LinkedIn', link=linkedin, justify='left')
             .grid(row=4, column=0, sticky='w', padx=10, pady=(0, 10)))
        else:
            ctk.CTkLabel(self, text='').grid(row=4, column=0, sticky='w', padx=10, pady=(0, 10))


class WrappingLabel(ctk.CTkLabel):
    labels = []

    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, justify='left', **kwargs)
        self.old_width = 0
        self.configure(wraplength=800)
        WrappingLabel.labels.append(self)


class AboutPage(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        summary_text = "The Gravity Wave Analysis Tool (GWAT) is a cross-platform software application that is " \
                       "designed to graph and analyze radiosonde data. It offers an intuitive interface for " \
                       "meteorologists, researchers, and students, making it accessible to those without programming " \
                       "knowledge or money to burn (college students). The Gravity Wave Analysis Tool simplifies the " \
                       "process of examining atmospheric data, providing powerful analysis with ease."

        h1_font = ctk.CTkFont(size=32, weight='bold')
        h2_font = ctk.CTkFont(size=24, weight='bold')
        h3_font = ctk.CTkFont(size=16)
        citation_font = ctk.CTkFont(slant='italic')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.current_row = 0

        def next_row():
            self.current_row += 1
            return self.current_row

        # about us
        about_us = ctk.CTkLabel(self, text="About The project", font=h1_font)
        about_us.grid(row=next_row(), column=0, columnspan=4, sticky='ew')

        summary = WrappingLabel(self, text=summary_text)
        summary.grid(row=next_row(), column=0, columnspan=4, sticky='w', padx=10, pady=(20, 10))

        HyperlinkLabel(self, text="User manual", link="https://github.com/gravitywaveanalysistool/gwat/wiki",
                       justify='left').grid(row=next_row(), column=0, columnspan=4, sticky='w', padx=10)

        # authors
        authors = ctk.CTkLabel(self, text="Authors", font=h2_font, justify='left')
        authors.grid(row=next_row(), column=0, columnspan=4, sticky='w', padx=10, pady=(20, 10))

        author_row = next_row()
        (AuthorCard(self,
                    'Tyler Cullen',
                    'cullentyler95@gmail.com',
                    'https://www.linkedin.com/in/tfcullen/',
                    'https://github.com/cullentyler95',
                    datapath.getDataPath('media/tyler.png'))
         .grid(row=author_row, column=0, sticky='ew', padx=10))
        (AuthorCard(self,
                    'Jeremiah Hubbard',
                    'jjhh12@outlook.com',
                    None,
                    'https://github.com/piesarentsquare',
                    datapath.getDataPath('media/jeremiah.jpg'))
         .grid(row=author_row, column=1, sticky='ew', padx=(0, 10)))
        (AuthorCard(self,
                    'Eric Stewart',
                    'ericjamestewart@gmail.com',
                    None,
                    'https://github.com/estewar5',
                    datapath.getDataPath('media/logo_notext.png'))
         .grid(row=author_row, column=2, sticky='ew', padx=(0, 10)))
        (AuthorCard(self,
                    'Scott Wilmot',
                    'scottwilmot04@gmail.com',
                    None,
                    'https://github.com/Gooseclemons',
                    datapath.getDataPath('media/scott.png'))
         .grid(row=author_row, column=3, sticky='ew', padx=(0, 10)))

        # license
        license_title = ctk.CTkLabel(self, text="License", font=h2_font, justify='left')
        license_title.grid(row=next_row(), column=0, columnspan=4, sticky='w', padx=10, pady=(20, 0))

        license_link = HyperlinkLabel(self,
                                      text="GPL-3.0 License",
                                      link="https://github.com/gravitywaveanalysistool/gwat/blob/main/LICENSE",
                                      justify='left')
        license_link.grid(row=next_row(), column=0, columnspan=4, sticky='w', padx=10)

        # credits
        credits_title = ctk.CTkLabel(self, text="Credits", font=h2_font, justify='left')
        credits_title.grid(row=next_row(), column=0, columnspan=4, sticky='w', padx=10, pady=(20, 0))

        with open(datapath.getDataPath('credits.json')) as f:
            credit_json = json.load(f)
            for (credit, params) in credit_json['credits'].items():
                (ctk.CTkLabel(self, text=credit, justify='left', font=h3_font)
                 .grid(row=next_row(), column=0, columnspan=4, sticky='w', padx=10))

                if 'citation' in params:
                    (WrappingLabel(self, text=params['citation'], font=citation_font)
                     .grid(row=next_row(), column=0, columnspan=4, sticky='w', padx=20))

                if 'link' in params:
                    (HyperlinkLabel(self, text=params['link'], link=params['link'], justify='left')
                     .grid(row=next_row(), column=0, columnspan=4, sticky='w', padx=20))

            (ctk.CTkLabel(self, text='Libraries', font=h2_font, justify='left')
             .grid(row=next_row(), column=0, columnspan=4, sticky='w', padx=10, pady=(20, 0)))

            row = next_row()
            column = 0
            for (credit, link) in credit_json['pip-dependencies'].items():
                (HyperlinkLabel(self, text=credit, link=link)
                 .grid(row=row, column=column, columnspan=2, sticky='w', padx=10))
                column += 2
                if column == 4:
                    row += 1
                    column = 0


class AboutFrame(ctk.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("About")
        self.geometry("800x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.bind('<Configure>', self.on_resize)

        self.scroll_window = AboutPage(self)
        self.scroll_window.grid(row=0, column=0, sticky='nsew')

        self.lift()
        self.grab_set()

    def on_resize(self, event):
        if event.widget.widgetName != self.widgetName:
            return
        for label in WrappingLabel.labels:
            label.configure(wraplength=(event.width / ScalingTracker.get_window_dpi_scaling(self)) - 40)
