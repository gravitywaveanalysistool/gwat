import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import test


def display_parameters_in_root(station, parent):
    # Create a frame to contain the treeview and scrollbars
    param_frame_container = Frame(parent)

    # Create the tree view frame and scrollbars
    param_frame = ttk.Treeview(param_frame_container)
    tree_y_scrollbar = Scrollbar(param_frame_container, orient=VERTICAL, command=param_frame.yview)
    tree_x_scrollbar = Scrollbar(param_frame_container, orient=HORIZONTAL, command=param_frame.xview)

    # Set the scroll commands to come from scroll bars
    param_frame.config(yscrollcommand=tree_y_scrollbar.set)
    param_frame.config(xscrollcommand=tree_x_scrollbar.set)

    # Insert DataFrame columns as treeview columns
    param_frame["columns"] = list(station.profile_df.columns)
    for column in station.profile_df.columns:
        param_frame.heading(column, text=column)

    # Insert DataFrame rows as treeview items
    for i, row in station.profile_df.iterrows():
        param_frame.insert("", tkinter.END, values=list(row))

    # Pack all our frames to the container
    tree_y_scrollbar.pack(side="right", fill="y")
    tree_x_scrollbar.pack(side="bottom", fill="x")
    param_frame.pack(padx=5, pady=5, expand=True, fill="both")

    # Pack our container frames
    param_frame_container.pack(side="right", anchor="se", fill="both")


def graph2d(x, y, deg, x_label, y_label, title):
    # Scatter plot
    fig = plt.figure()
    plt.scatter(x, y, s=5, label='Data points')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    return fig


def display_graphs_in_root(station, parent):
    graph_frame_container = ttk.Frame(parent)
    fig = graph2d(station.profile_df['T'] + 273, station.profile_df['Alt'] / 1000, 3, 'Temperature (K)',
                  'Altitude (km)',
                  'Temperature Profile and Fit')

    canvas = FigureCanvasTkAgg(fig, master=graph_frame_container)
    canvas.draw()
    canvas.get_tk_widget().pack()

    graph_frame_container.pack(side="right", anchor="ne", fill="both")


def main():
    # vars
    stations = []

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
        file_path = filedialog.askopenfilename()
        station = test.generate_profile_data(file_path)
        stations.append(station)
        station_list.insert(END, station.station_name)

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

    # This executes whenever we select a station on the list, this will handle graph display and param display
    def on_station_select(event):
        selected_index = station_list.curselection()
        if selected_index:
            selected_station_name = station_list.get(selected_index)
            selected_station = None
            for station in stations:
                if station.station_name == selected_station_name:
                    selected_station = station
                    break
            if selected_station:
                display_parameters_in_root(selected_station, root)
                display_graphs_in_root(selected_station, root)

    # Bind the selection event to the Listbox
    station_list.bind("<<ListboxSelect>>", on_station_select)

    # Pack list frame
    list_frame.pack(side="left", fill="both")

    root.mainloop()


if __name__ == "__main__":
    main()
