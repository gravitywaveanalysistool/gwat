import subprocess
from src import utils
import os
from src import datapath


def detect_gdl_idl():
    try:
        subprocess.run(['gdl', '-v'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return 'gdl'
    except:
        try:
            subprocess.run(['idl', '-v'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return 'idl'
        except:
            return 'none'


class GDLError(Exception):
    pass


def create_gdl_friendly_file(df):
    filename = utils.get_temp_folder() + 'gdl_friendly_profile.txt'
    f = open(filename, 'w', encoding='ISO-8859-1')
    # skip 20 lines
    for i in range(0, 20):
        # ISO-8859-1 needs carriage returns
        f.write('filler\n')

    def v_or(row, key, default):
        if key in row:
            return row[key]
        return default

    for i, row in df.iterrows():
        f.write(str(int(v_or(row, 'Time', 9999.0))).ljust(24) + '\t')
        f.write(str(v_or(row, 'P', 9999.0)).ljust(6) + '\t')
        f.write(str(v_or(row, 'T', 999.0)).ljust(23) + '\t')
        f.write(str(v_or(row, 'Hu', 999.0)).ljust(24) + '\t')
        f.write(str(v_or(row, 'Ws', 999.0)).ljust(5) + '\t')
        f.write(str(v_or(row, 'Wd', 999.0)).ljust(23) + '\t')
        f.write(str(v_or(row, 'Long.', 999.0)).ljust(10) + '\t')
        f.write(str(v_or(row, 'Lat.', 999.0)).ljust(13) + '\t')
        f.write(str(v_or(row, 'Alt', 999.0)).ljust(7) + '\t')
        f.write(str(v_or(row, 'Geopot', 99999.0)).ljust(12) + '\t')
        f.write(str(v_or(row, 'MRI', 999.0)).ljust(10) + '\t')
        f.write(str(v_or(row, 'RI', 999.0)).ljust(10) + '\t')
        f.write(str(v_or(row, 'Dewp.', 999.0)).ljust(8) + '\t')
        f.write(str(v_or(row, 'Virt. Temp', 999.0)).ljust(14) + '\t')
        f.write(str(v_or(row, 'Rs', 999.0)).ljust(5) + '\t')
        f.write(str(v_or(row, 'Elevation', 999.0)).ljust(9) + '\t')
        f.write(str(v_or(row, 'Azimuth', 999.0)).ljust(8) + '\t')
        f.write(str(v_or(row, 'Range', 999.0)).ljust(7) + '\t')
        f.write(str(v_or(row, 'D', 999.0)))
        f.write('\n')

    for i in range(0, 10):
        f.write('end\n')
        
    f.close()

    return filename


def run_gdl(filepath, latitude, gdl_or_idl):
    """
    @param filepath: path to the input file
    @param latitude: latitude parameter extracted from the input file
    @param gdl_or_idl: the gw_eclipse.pro runner, either 'gdl' or 'idl'
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
