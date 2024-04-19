import subprocess
from ui import errorframe
from utils import get_temp_folder
import os
from src import datapath


def detect_gdl_idl():
    try:
        subprocess.run(['gdl', '-v'])
        return 'gdl'
    except:
        try:
            subprocess.run(['idl', '-v'])
            return 'idl'
        except:
            return 'none'


def runGDL(filepath, latitude, gui, gdl_or_idl):
    """
    @param filepath:
    @param latitude:
    @param gui:
    @return:
    """
    # Move to pro directory for access to gw programs
    cwd = os.getcwd()
    os.chdir(datapath.getProPath(""))  # Assumes we are running out of root directory

    # Start GDL
    process = subprocess.Popen([gdl_or_idl], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True)

    outfile = get_temp_folder() + "gw_parameters.txt"

    # Command list for execution
    commands = f"gw_eclipse_new,'{filepath}','{outfile}',{latitude}\nexit\n"

    # Run the commands and split into output and error for convenience
    output, error = process.communicate(input=commands)

    os.chdir(cwd)

    if output == "success\n":
        return 0
    else:
        print(filepath)
        errorframe.ErrorFrame(gui).showerror("Cannot Produce GDL Parameters for this file.")
