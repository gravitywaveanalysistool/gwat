import pandas as pd
import numpy as np
import matplotlib
from tabulate import tabulate
import matplotlib.pyplot as plt
from station import Station

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


def generate_profile_data(path_name):
    header_start_line, header_end_line = headerData(path_name)
    if header_start_line is not None and header_end_line is not None:
        nrows_to_read = header_end_line - header_start_line
        header_df = pd.read_csv(path_name, sep='\t', skiprows=header_start_line, nrows=nrows_to_read, engine='python', encoding='ISO-8859-1', header=None)

    profile_start_line, profile_end_line = grabProfileData(path_name)
    if profile_start_line is not None and profile_end_line is not None:
        nrows_to_read = profile_end_line - profile_start_line
        profile_df = pd.read_csv(path_name, sep='\t', skiprows=profile_start_line, nrows=nrows_to_read, engine='python', encoding='ISO-8859-1')
        #profile_df.columns += profile_df.iloc[0]
        profile_df.rename(columns=lambda x: x.strip(), inplace=True)
        profile_df = profile_df[1:]
    #print(tabulate(profile_df, headers="keys"))

    tropo_start_line, tropo_end_line = tropoData(path_name)
    if tropo_start_line is not None and tropo_end_line is not None:
        nrows_to_read = tropo_end_line - tropo_start_line
        tropo_df = pd.read_csv(path_name, sep='\t', skiprows=tropo_start_line, nrows=nrows_to_read, engine='python', encoding='ISO-8859-1')
    # Converts column to whatever integer equivalent float / int
    for col in profile_df.select_dtypes(include=['object']).columns:
        profile_df[col] = pd.to_numeric(profile_df[col], downcast='integer')

    # Calculates the difference between followings alts
    profile_df['diff'] = profile_df['Alt'].diff()
    peak_index = profile_df[profile_df['diff'] < 0].first_valid_index()
    # Drop rows after peak and drop diff column
    if peak_index is not None:
        profile_df = profile_df.loc[:peak_index - 1]
    profile_df = profile_df.drop(columns=['diff'])
    station = Station(path_name, profile_df, tropo_df, header_df)
    return station