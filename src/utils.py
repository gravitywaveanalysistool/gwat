import json

from matplotlib.backends.backend_pdf import PdfPages
import os

from src import datapath
import platform


def get_temp_folder():
    path = ""
    if platform.system() == 'Windows':
        path = 'C:\\Users\\' + os.getlogin() + '\\AppData\\Local\\Temp\\'
    else:
        path = '/tmp/'
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


def get_parameter_file():
    return os.path.abspath(get_temp_folder() + 'gw_parameters.txt')


class MalformedFileError(Exception):
    pass


def read_params():
    """
    @return:
    """

    if not os.path.isfile(get_parameter_file()):
        raise FileNotFoundError

    f = open(get_parameter_file(), "r")

    paramNames = ["Horizontal Wavelength", "Vertical Wavelength", "Mean Phase Propogation Direction",
                  "Upward Propogation Fraction",
                  "Zonal Momentum Flux", "Meridional Momentum Flux", "Potential Energy", "Kinetic Energy"]
    units = ["[km]", "[km]", "[deg]", " ", "[m^2/s^2]", "[m^2/s^2]", "[J/kg]", "[J/kg]"]
    allParams = []
    tropoParams = {}
    stratoParams = {}

    for line in f:
        allParams.append(line.strip())

    if len(allParams) != len(paramNames) * 2:
        f.close()
        raise MalformedFileError

    for i, _ in enumerate(allParams):
        if i == len(paramNames):
            break
        tropoParams[paramNames[i]] = allParams[i] + " " + units[i]
        stratoParams[paramNames[i]] = allParams[i + len(paramNames)] + " " + units[i]

    f.close()

    return tropoParams, stratoParams


def save_params_to_file(strato_params, tropo_params, file_path):
    """
    Parameters are stored in UI as a Python dictionary with ParameterName -> Value
    Need: output file path, parameter dictionary
    """

    file = open(file_path, 'w')

    def max_length(s):
        return max(map(len, map(str, s)))

    longest_key_length = max(max_length(tropo_params.keys()), max_length(strato_params.keys()))
    longest_value_length = max(max_length(tropo_params.values()), max_length(strato_params.values()))
    row_width = longest_key_length + longest_value_length + 4

    def write_kv(dictionary):
        for key, value in dictionary.items():
            # Controls how much to indent the value as to line up values in a column
            padding = row_width - len(str(value))
            line = key.ljust(padding) + str(value)
            file.write(line + "\n")

    file.write("Stratosphere:\n")
    write_kv(strato_params)
    file.write("\nTroposphere:\n")
    write_kv(tropo_params)
    file.close()


def save_graph_to_file(graph_objects, file_path, selected_graphs):
    """
    - This function requires a list of desired graphs to be input which should be passed from the UI
    when the user checks off the graphs they want to export
    - Graphs will then be exported to a single pdf file
    - Defaults to pdf but further file types can be added later if needed
    """

    # if selection is empty, or the intersection of the graphs and selections is empty
    if not selected_graphs or len(set(graph_objects.keys()) & set(selected_graphs)) == 0:
        return

    out_file = PdfPages(file_path)  # Creates the output file

    for name in selected_graphs:  # Saves each graph to file
        if name not in graph_objects:
            continue
        out_file.savefig(graph_objects[name].get_figure("strato", export=True))
        out_file.savefig(graph_objects[name].get_figure("tropo", export=True))

    out_file.close()


def save_graphs_as_png(graph_objects, folder_path, selected_graphs):
    """
    - This function saves the selected graphs as individual PNG files to a directory of the users choice
    - Very not complete at the moment
    """
    if not selected_graphs or len(set(graph_objects.keys()) & set(selected_graphs)) == 0:
        return

    png_folder = os.path.join(folder_path, "graphs")
    if not os.path.exists(png_folder):
        os.mkdir(png_folder)

    for name in selected_graphs:
        graph_objects[name].get_figure("strato", export=True).savefig(os.path.join(png_folder, name + "-stratosphere"))
        graph_objects[name].get_figure("tropo", export=True).savefig(os.path.join(png_folder, name + "-troposphere"))


def save_options(options):
    with open(datapath.getDataPath("options.json"), 'w') as f:
        json.dump(options, f)


def load_options():
    with open(datapath.getDataPath("options.json"), 'r') as f:
        return json.load(f)
