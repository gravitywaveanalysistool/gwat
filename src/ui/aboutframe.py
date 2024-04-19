import customtkinter as ctk

def open_link(link):
    pass

class CreditTabs(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.add("About")
        self.add("Credits")
        self.add("License")
        self.add("Libraries")

        # About Text
        self.abouttext = ctk.CTkTextbox(master=self.tab("About"))
        self.abouttext.pack(fill="both", expand=True)
        self.abouttext.insert("0.0", "GWAT is a tool developed to analyze and visualize gravity "
                                "waves using data gathered from radiosonde launches. This tool eliminates the need to"
                                " interface with the IDL/GDL command-line for under-graduate STEM students.")

        self.abouttext.insert("4.0", "\n\nGithub: https://github.com/PiesArentSquare/csc380-team-e")

        # Add a tag to the link text
        # self.abouttext.tag_add("link", "4.0", "4.51")  # Assuming link text starts at line 9, column 0 and ends at line 9, column 51
        #
        # # Configure the tag to make it clickable
        # self.abouttext.tag_config("link", foreground="blue", underline=True)
        #
        # # Bind the click event to the tag
        # self.abouttext.tag_bind("link", "<Button-1>", open_link)

        # Credits Text
        self.creditstext = ctk.CTkTextbox(master=self.tab("Credits"))
        self.creditstext.pack(fill="both", expand=True)
        self.creditstext.insert("0.0", "Authors:\n\n"
                                       "Tyler Cullen: tcullen@oswego.edu\n"
                                       "Jeremiah Hubbard: jhubbar4@oswego.edu\n"
                                       "Eric Stewart: estewar5@oswego.edu\n"
                                       "Scott Wilmot: swilmot@oswego.edu")


class AboutFrame(ctk.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("About")
        self.geometry("500x400")
        self.tab_view = CreditTabs(master=self)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)

        self.lift()
        self.grab_set()
