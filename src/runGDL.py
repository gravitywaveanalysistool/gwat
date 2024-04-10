import subprocess
from ui import errorframe
from utils import get_temp_folder
import os
from src import datapath


def detect_gdl_idl():
    if subprocess.run(['gdl', '-v']).returncode == 0:
        return 'gdl'
    elif subprocess.run(['idl', '-v']).returncode == 0:
        return 'idl'
    else:
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
        errorframe.ErrorFrame(gui).showerror("Bad Input File.")
