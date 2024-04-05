import subprocess
from ui import errorframe
import os

def runGDL(filepath, latitude, gui):
    # Move to pro directory for access to gw programs
    os.chdir("pro") # Assumes we are running out of root directory

    # Start GDL
    process = subprocess.Popen(['gdl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Command list for execution
    commands = f"gw_eclipse_new,'{filepath}',{latitude}\nexit\n"

    # Run the commands and split into output and error for convenience
    output, error = process.communicate(input=commands)

    if output == "success\n":
        return 0
    else:
        errorframe.ErrorFrame(gui).showerror("Bad Input File.")