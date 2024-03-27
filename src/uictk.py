from tkinter import filedialog

import pandas as pd
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import test
import graphs
from src import exportGraphs


class ErrorFrame(customtkinter.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.button = None
        self.text_dialog = None
        self.title("Error")
        self.lift()

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

    def update_geometry(self):
        self.update_idletasks()
        width = self.winfo_reqwidth() + 20
        height = self.winfo_reqheight() + 20
        self.geometry(f"{width}x{height}")

class CustomGraphFrame(customtkinter.CTkToplevel):
    def __init__(self, master, station, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.button = None
        self.text_dialog = None
        self.title("Error")
        self.lift()


        #self.text_dialog = customtkinter.CTkLabel(self, text=message)
        #self.text_dialog.grid(row=0, column=0, sticky="N", padx=20, pady=20)

        # Convert labels to a list
        label_list = station.profile_df.loc[0, :].values.flatten().tolist()

        # Choose X DropDown
        self.choose_x = customtkinter.CTkOptionMenu(self, values=label_list)
        self.choose_x.grid(row=0, column=0, sticky="N", padx=20, pady=20)

        # Choose Y DropDown
        self.choose_y = customtkinter.CTkOptionMenu(self, values=label_list)
        self.choose_y.grid(row=0, column=0, sticky="N", padx=20, pady=20)

        # Choose best fit degree
        self.choose_bf = customtkinter.CTkEntry(self, )
        self.choose_bf.grid(row=0, column=0, sticky="N", padx=20, pady=20)

        def close_window():
            self.destroy()

        self.button = customtkinter.CTkButton(self, text="Create", command=close_window)
        self.button.grid(row=1, column=0, padx=20, pady=10)


class ParameterFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, params, **kwargs):
        super().__init__(master, **kwargs)

        self.params = params

        for i, (label, param) in enumerate(params.items()):
            self.add_item(i, label, param)

    def add_item(self, i, label, param):
        label = customtkinter.CTkLabel(self, text=label)
        param = customtkinter.CTkLabel(self, text=param)

        label.grid(row=i, column=0, pady=(0, 10), padx=(0, 10), sticky="w")
        param.grid(row=i, column=1, pady=(0, 10), padx=(0, 10), sticky="e")


class ScrollingCheckButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, figs, check_cmd=None, but_cmd=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        self.check_cmd = check_cmd
        self.but_cmd = but_cmd
        self.radiobutton_variable = customtkinter.StringVar()
        self.button_list = []
        self.checkbox_dict = {}
        for title, fig in figs.items():
            self.add_item(title)  # Add the title to your UI

    def add_item(self, item):
        button = customtkinter.CTkButton(self, text=item, width=100, height=24)
        checkbox = customtkinter.CTkCheckBox(self, text="", width=10)
        if self.but_cmd and self.check_cmd is not None:
            button.configure(command=lambda: self.but_cmd(item))
            checkbox.configure(command=self.check_cmd)
        checkbox.grid(row=len(self.checkbox_dict), column=0, pady=(0, 10), sticky="e")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), sticky="w")

        self.button_list.append(button)
        self.checkbox_dict[item] = checkbox

    def remove_item(self, item):
        for button, checkbox in zip(self.button_list, self.checkbox_dict):
            if item == button.cget("text"):
                button.destroy()
                checkbox.destroy()

                self.button_list.remove(button)
                self.checkbox_dict.pop(item)
                return


class GraphFrame(customtkinter.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Create a canvas to display the plot
        self.canvas = customtkinter.CTkCanvas(self)
        self.canvas.grid(row=0, column=0, padx=15, pady=15)

    def draw_plot(self, fig):
        self.canvas.delete('all')
        self.canvas.fig_agg = FigureCanvasTkAgg(fig, master=self.canvas)
        self.canvas.fig_agg.draw()
        self.canvas.fig_agg.get_tk_widget().pack(fill=customtkinter.BOTH, expand=True)


class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # vars
        self.checkbox_dict = None
        self.graph_frame = None
        self.param_frame = None
        file_path = None
        figs = {}

        self.title("Gravity Wave Analysis Tool")
        self.geometry("1200x800")

        # Allow upload button to expand anywhere
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        def export_graphs():
            nonlocal file_path
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf")

            if file_path:
                exportGraphs.save_file(figs, file_path, self.checkbox_dict, self)

        def export_params():
            file = filedialog.asksaveasfile(defaultextension=".txt")
            if file:
                for i, (label, param) in enumerate(self.param_frame.params.items()):
                    file.write(label + ',' + param + '\n')

        def create_custom_graph():
            # Have list of params stored somewhere
            # Have dropdown list that shows the options for axis
            # List of graph type
            # Fields for x,y title

            raise NotImplementedError("Eric")

        def list_checkmark_event():
            pass

        def list_button_event(title):
            fig = figs[title]
            if self.graph_frame:
                self.graph_frame.destroy() # COME BACK TO THIS!!!!!!!!!!!
            self.graph_frame = GraphFrame(master=self)
            self.graph_frame.grid(row=0, column=1, padx=15, pady=15, rowspan=3, sticky="ne")
            self.graph_frame.draw_plot(fig)

        def generate_graphs(station):
            # Create a list of graph figures from the station list
            figs['Temperature Profile and Fit'] = (graphs.graph2d((pd.to_numeric(station.profile_df['T']) + 273),
                                                                  (pd.to_numeric(station.profile_df['Alt']) / 1000),
                                                                  6,
                                                                  'Temperature (K)',
                                                                  'Altitude (km)',
                                                                  'Temperature Profile and Fit'))

            figs['Wind Speed Profile and Fit'] = graphs.graph2d(pd.to_numeric(station.profile_df['Ws']),
                                                                pd.to_numeric(station.profile_df['Alt']),
                                                                8,
                                                                'Wind Speed',
                                                                'Altitude',
                                                                'Wind Speed Profile and Fit')
            figs['Hodograph 1'] = graphs.hodograph(40, 2, station.profile_df)
            # figs['Hodograph 2'] = graphs.hodograph(30, 1, station.profile_df)

        def upload_file():
            nonlocal file_path
            file_path = filedialog.askopenfilename()

            if file_path:
                station = test.generate_profile_data(file_path)

                # GENERATE GRAPHS
                generate_graphs(station)

                # Make upload button not expand
                self.grid_columnconfigure(0, weight=0)
                self.grid_rowconfigure(0, weight=0)

                # Make Custom button not expand
                self.grid_rowconfigure(1, weight=0)

                # Make Export button not expand
                self.grid_rowconfigure(3, weight=0)

                # Allow scroll frame to expand
                self.grid_rowconfigure(2, weight=1)

                # Create scrollable checkbox frame
                self.scrollable_frame = ScrollingCheckButtonFrame(master=self, width=300,
                                                                  check_cmd=list_checkmark_event,
                                                                  but_cmd=list_button_event,
                                                                  figs=figs)
                self.scrollable_frame.grid(row=2, column=0, padx=15, pady=15, rowspan=2, sticky="nsew")
                self.checkbox_dict = self.scrollable_frame.checkbox_dict

                # Create Custom Graph Button
                self.upload_button = customtkinter.CTkButton(self, text="Custom Graph", command=create_custom_graph)
                self.upload_button.grid(row=1, column=0, padx=15, pady=15)

                # Create Export Graph Button
                self.upload_button = customtkinter.CTkButton(self, text="Export Graph(s)", command=export_graphs)
                self.upload_button.grid(row=4, column=0, padx=15, pady=15)

                # Create Export Params Button
                self.upload_button = customtkinter.CTkButton(self, text="Export Params", command=export_params)
                self.upload_button.grid(row=4, column=1, padx=15, pady=15)

                # Create Param Frame
                params = {}
                for i in range(10):
                    params[f"Param {i}"] = f"value {i}"

                self.param_frame = ParameterFrame(master=self, params=params, width=600)
                self.param_frame.grid(row=3, column=1, padx=15, pady=15, sticky="sew")
                # self.grid_rowconfigure((1, 3), weight=0)

        # Button for uploading file
        self.upload_button = customtkinter.CTkButton(self, text="Upload File", command=upload_file)
        self.upload_button.grid(row=0, column=0, padx=15, pady=15)

        ErrorFrame(self).showerror("Test")


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = GUI()
    app.mainloop()
