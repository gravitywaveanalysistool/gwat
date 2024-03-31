from matplotlib.backends.backend_pdf import PdfPages

from src.ui import uictk


def save_params_to_file(parameterDictionary, filePath):
    """
    Parameters are stored in UI as a Python dictionary with ParameterName -> Value
    Need: output file path, parameter dictionary
    To add: right alignment needed for larger values to prevent key-value clipping in output
    """
    file = open(filePath, 'w')
    longestKeyName = 0  # For keeping track of how much to indent value
    for key in parameterDictionary:
        if len(key) > longestKeyName:
            longestKeyName = len(key)

    for key, value in parameterDictionary.items():
        difference = longestKeyName - len(key)  # Controls how much to indent the value as to line up values in a column
        line = key + ("{:>" + str(difference+8) + "}").format(str(value)) # +8 is an output formatting preference
        file.write(line + "\n")
    file.close()


# Talk to Eric to see how he's handling the desired graphs from UI
def save_graph_to_file(graphs, file_path, checkbox_dict, gui):
    """
    - This function requires a list of desired graphs to be input which should be passed from the UI
    when the user checks off the graphs they want to export
    - Graphs will then be exported to a single pdf file
    - Defaults to pdf but further file types can be added later if needed
    """
    if not checkbox_dict:
        uictk.ErrorFrame(gui).showerror("No Graphs Selected!")
    else:
        out_file = PdfPages(file_path)  # Creates the output file

        for name, checkbox in checkbox_dict.items():  # Saves each graph to file
            if checkbox.get():
                out_file.savefig(graphs[name])

        out_file.close()
