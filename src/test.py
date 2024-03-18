import pandas as pd
import numpy as np
import matplotlib
from tabulate import tabulate
import matplotlib.pyplot as plt

rawData = './Tolten_Profile/T3_1800_12132020_Artemis_Rerun.txt'


# grab header information such as station name date etc...
def headerData(rawData, encoding='ISO-8859-1'):
    start_line = None
    end_line = None
    with open(rawData, 'r', encoding=encoding) as file:
        headerDataHit = False
        for i, line in enumerate(file):
            if 'Launch Date:' in line:
                headerDataHit = True
            elif headerDataHit and 'Profile Data:' in line:
                end_line = i
                break
            elif headerDataHit and line.strip() and start_line is None:
                # Grabs line where profile data exists
                start_line = i - 1
    return start_line, end_line


# grab main data to be graphed which is the profile data
def grabProfileData(rawData, encoding='ISO-8859-1'):
    start_line = None
    end_line = None
    with open(rawData, 'r', encoding=encoding) as file:
        pfDataHit = False
        for i, line in enumerate(file):
            if 'Profile Data' in line:
                pfDataHit = True
            elif pfDataHit and 'Tropopauses:' in line:
                # Mark the line before Tropopauses footer
                end_line = i - 1
                break
            elif pfDataHit and line.strip() and start_line is None:
                # Grabs line where profile data exists
                start_line = i
    return start_line, end_line


# grab troposphere data
def tropoData(rawData, encoding='ISO-8859-1'):
    start_line = None
    end_line = None
    with open(rawData, 'r', encoding=encoding) as file:
        tropoDataHit = False
        for i, line in enumerate(file):
            if '1. Tropopause:' in line:
                tropoDataHit = True
            elif tropoDataHit and 'Reason of Stop Sounding:' in line:
                end_line = i
                break
            elif tropoDataHit and line.strip() and start_line is None:
                # Grabs line where profile data exists
                start_line = i - 1
    return start_line, end_line

data_start_line, data_end_line = headerData(rawData)
if data_start_line is not None and data_end_line is not None:
    nrows_to_read = data_end_line - data_start_line
    header_df = pd.read_csv(rawData, sep='\t', skiprows=data_start_line, nrows=nrows_to_read, engine='python', encoding='ISO-8859-1', header=None)
data_start_line, data_end_line = grabProfileData(rawData)
if data_start_line is not None and data_end_line is not None:
    nrows_to_read = data_end_line - data_start_line
    profile_df = pd.read_csv(rawData, sep='\t', skiprows=data_start_line, nrows=nrows_to_read, engine='python', encoding='ISO-8859-1')
    #profile_df.columns += profile_df.iloc[0]
    profile_df.rename(columns=lambda x: x.strip(), inplace=True)
    profile_df = profile_df[1:]
print(tabulate(profile_df, headers="keys"))


data_start_line, data_end_line = tropoData(rawData)
if data_start_line is not None and data_end_line is not None:
    nrows_to_read = data_end_line - data_start_line
    tropo_df = pd.read_csv(rawData, sep='\t', skiprows=data_start_line, nrows=nrows_to_read, engine='python', encoding='ISO-8859-1')