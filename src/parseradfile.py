import numpy as np
import pandas as pd
from src.station import Station

rawData = './Tolten_Profile/T3_1800_12132020_Artemis_Rerun.txt'


# Grab header information such as station name date etc...
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
                #Grabs line where profile data exists
                start_line = i  - 1
    return start_line, end_line


# Grab profile data which is what contains the raw Radiosonde data
def grabProfileData(rawData, encoding='ISO-8859-1'):
    start_line = None
    end_line = None
    with open(rawData, 'r', encoding=encoding) as file:
        pfDataHit = False
        for i, line in enumerate(file):
            if 'Profile Data' in line:
                pfDataHit = True
            elif pfDataHit and 'Tropopauses:' in line:
                #Mark the line before Tropopauses footer
                end_line = i - 1
                break
            elif pfDataHit and line.strip() and start_line is None:
                #Grabs line where profile data exists
                start_line = i
    return start_line, end_line


def get_tropopause_value(file_path):
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        lines = file.readlines()
        tropopause_found = False
        for i, line in enumerate(lines):
            if "Tropopauses:" in line:
                tropopause_found = True
            if tropopause_found and "1.:" in line:
                value = line.split("1.:")[1].split()[0]
                return float(value)
                break

def calcWindComps(dataframe, speeds, directions):
    speeds = np.array(dataframe[speeds])
    directions = np.array(dataframe[directions])

    u = -speeds * np.sin(np.radians(directions))
    v = -speeds * np.cos(np.radians(directions))
    dataframe['U'] = u
    dataframe['V'] = v

def generate_profile_data(path_name):
    data_start_line, data_end_line = headerData(path_name)
    if data_start_line is not None and data_end_line is not None:
        nrows_to_read = data_end_line - data_start_line
        header_df = pd.read_csv(path_name, sep='\t', skiprows=data_start_line, nrows=nrows_to_read, engine='python',
                                encoding='ISO-8859-1', header=None)

    data_start_line, data_end_line = grabProfileData(path_name)
    if data_start_line is not None and data_end_line is not None:
        nrows_to_read = data_end_line - data_start_line
        profile_df = pd.read_csv(path_name, sep='\t', skiprows=data_start_line, nrows=nrows_to_read, engine='python',
                                 encoding='ISO-8859-1')
        # profile_df.columns += profile_df.iloc[0]
        profile_df.rename(columns=lambda x: x.strip(), inplace=True)
        profile_df = profile_df[1:]

    # Converts column to whatever integer equivalent float / int
    for col in profile_df.select_dtypes(include=['object']).columns:
        profile_df[col] = pd.to_numeric(profile_df[col], downcast='integer')

    mean_temp = profile_df['T'].mean()
    profile_df['T_Perturbation'] = profile_df['T'] - mean_temp

    Tropopause = get_tropopause_value(path_name)
    closest_index = (profile_df['P'] - Tropopause).abs().idxmin()
    tropo_df = profile_df.iloc[:closest_index + 1]
    strato_df = profile_df.iloc[closest_index + 1:]

    # Calculates the difference between followings alts
    profile_df['Ascending_Rate'] = profile_df['Alt'].diff()
    peak_index = profile_df[profile_df['Ascending_Rate'] < 0].first_valid_index()
    # Drop rows after peak and drop diff column
    if peak_index is not None:
        profile_df = profile_df.loc[:peak_index - 1]

    calcWindComps(profile_df, 'Ws', 'Wd')
    calcWindComps(tropo_df, 'Ws', 'Wd')
    calcWindComps(strato_df, 'Ws', 'Wd')

    station = Station(path_name, profile_df, strato_df, tropo_df, header_df)
    return station



