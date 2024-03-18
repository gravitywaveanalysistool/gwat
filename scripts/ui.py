from tkinter import *
from tkinter import filedialog


def main():
    # Define the root frame
    root = Tk()
    root.title("Gravity Wave Analysis Tool")
    root.geometry("800x600")

    # Define our Frames
    list_frame = Frame(root)
    menu_bar = Menu(root)

    # -----MENUBAR-----
    # Create Import, Graph, and Export Menu's

    # Import Menu
    import_menu = Menu(menu_bar, tearoff=0)

    def import_files():
        file_path = filedialog.askopenfilenames()

    def import_directory():
        directory = filedialog.askdirectory()

    import_menu.add_command(label="File(s)", command=import_files)
    import_menu.add_command(label="Directory", command=import_directory)

    # Graph Menu
    graph_menu = Menu(menu_bar, tearoff=0)
    custom_menu = Menu(menu_bar, tearoff=0)
    custom_menu.add_command(label="XY Graph")
    custom_menu.add_command(label="Hodograph")
    graph_menu.add_cascade(label="Create Custom", menu=custom_menu)

    # Export Menu
    export_menu = Menu(menu_bar, tearoff=0)
    export_menu.add_command(label="Parameters")
    export_menu.add_command(label="Graphs")
    export_menu.add_command(label="All")

    # Options Menu
    options_menu = Menu(menu_bar, tearoff=0)

    # Add Cascades to Menu Bar
    menu_bar.add_cascade(label="Import", menu=import_menu)
    menu_bar.add_cascade(label="Graph", menu=graph_menu)
    menu_bar.add_cascade(label="Export", menu=export_menu)
    menu_bar.add_cascade(label="Options", menu=options_menu)

    # Add menu to Root
    root.config(menu=menu_bar)

    # -----STATION LIST-----
    # Create list and scrollbar
    station_list = Listbox(list_frame, width=25)
    list_scrollbar = Scrollbar(list_frame, orient=VERTICAL, command=station_list.yview)

    # Set scrollbar and listbox configurations
    station_list.config(yscrollcommand=list_scrollbar.set)

    # Pack listbox and scrollbar
    station_list.pack(side="left", fill="both", padx=5, pady=5)
    list_scrollbar.pack(side="right", fill="y")

    # Fill listbox with station names
    for i in range(1, 51):
        station_list.insert(END, f"Station {i}")

    # Pack list frame
    list_frame.pack(side="left", fill="both")





    root.mainloop()


if __name__ == "__main__":
    main()
