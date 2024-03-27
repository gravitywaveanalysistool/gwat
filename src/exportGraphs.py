"""
- This function requires a list of desired graphs to be input which should be passed from the UI
when the user checks off the graphs they want to export
- Graphs will then be exported to a single pdf file
- Defaults to pdf but further file types can be added later if needed
"""

from matplotlib.backends.backend_pdf import PdfPages

import uictk


# Talk to Eric to see how he's handling the desired graphs from UI
def save_file(graphs, file_path, checkbox_dict, gui):

    if not checkbox_dict:
        uictk.ErrorFrame(gui).showerror("No Graphs Selected!")
    else:
        out_file = PdfPages(file_path)  # Creates the output file

        for name, checkbox in checkbox_dict.items():  # Saves each graph to file
            if checkbox.get():
                out_file.savefig(graphs[name])

        out_file.close()
