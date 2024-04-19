import subprocess
from src import utils
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


class GDLError(Exception):
    pass

def runGDL(filepath, latitude, gdl_or_idl):
    """
    @param filepath:
    @param latitude:
    @param gui:
    @return:
    """
    filepath = os.path.abspath(filepath)

    if not os.path.isfile(filepath):
        raise FileNotFoundError

    # Move to pro directory for access to gw programs
    cwd = os.getcwd()
    os.chdir(datapath.getProPath(""))  # Assumes we are running out of root directory

    outfile = utils.get_parameter_file()

    # Start GDL
    process = subprocess.Popen([gdl_or_idl], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True)

    # Command list for execution
    commands = f"gw_eclipse_new,'{filepath}','{outfile}',{latitude}\nexit\n"

    # Run the commands and split into output and error for convenience
    output, error = process.communicate(input=commands)
    process.kill()

    os.chdir(cwd)

    if output != "success\n":
        os.remove(utils.get_parameter_file())
        raise GDLError
