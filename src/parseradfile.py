import numpy as np
import pandas as pd
from src.station import Station
from src import utils
import re

# Grab header information such as station name date etc...
def headerData(rawData, encoding='ISO-8859-1'):
    """
    @param rawData:
    @param encoding:
    @return:
    """
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
                start_line = i - 1
    return start_line, end_line


# Grab profile data which is what contains the raw Radiosonde data
def grabProfileData(rawData, encoding='ISO-8859-1'):
    """
    @param rawData:
    @param encoding:
    @return:
    """
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


def calc_tropopause(df, altitude_interval):
    # Define the bins for altitude
    max_altitude = df['Alt'].max()
    bins = np.arange(0, max_altitude + altitude_interval, altitude_interval)
    labels = bins[1:] - (altitude_interval / 2)  # Label each bin by the midpoint altitude
    df['Altitude Bin'] = pd.cut(df['Alt'], bins=bins, labels=labels, include_lowest=True)
    tropopause_df = df.groupby('Altitude Bin', observed=False).agg({'T': 'mean', "P": 'mean'}).reset_index()
    tropopause_df['Altitude Bin'] = tropopause_df['Altitude Bin'].astype(float)
    tropopause_df.rename(columns={'Altitude Bin': 'Alt', 'T': 'Mean Temperature'}, inplace=True)
    tropopause_df['Lapse Rate'] = tropopause_df['Mean Temperature'].diff() / 1

    # Identify potential tropopauses where lapse rate is between -2 and 2
    tropopause_df['Potential Tropopause'] = (tropopause_df['Lapse Rate'] >= -2) & (tropopause_df['Lapse Rate'] <= 2)
    tropopause_data = tropopause_df[(tropopause_df['Lapse Rate'] >= -2) & (tropopause_df['Lapse Rate'] <= 2)]
    tropopause_pressure = tropopause_data['P'].iloc[0] if not tropopause_data.empty else None

    return tropopause_pressure


def get_tropopause_value(file_path,df):
    """
    @param file_path:
    @return:
    """
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        lines = file.readlines()
        tropopause_found = False
        for i, line in enumerate(lines):
            if "Tropopauses:" in line:
                tropopause_found = True
            if tropopause_found and "1.:" in line:
                value = line.split("1.:")[1].split()[0]
                return float(value)
        return calc_tropopause(df, 1000)


def get_latitude_value(file_path):
    try:
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            # read entire file as string
            text = file.read()

        # Create regular expression to identify Latitude value
        regex_pattern = "Latitude:\s*(-?\d+\.\d+)"
        match = re.search(regex_pattern, text)

        # Return the matched reg expression if not a match return false
        return match.group(1) if match else -36
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
def calcWindComps(dataframe):
    """
    @param dataframe:
    @return:
    """
    dataframe["Wd_rad"] = np.deg2rad(dataframe["Wd"])
    dataframe['U'] = -dataframe['Ws'] * np.sin(dataframe['Wd_rad'])
    dataframe['V'] = -dataframe['Ws'] * np.cos(dataframe['Wd_rad'])

    coeff = np.polyfit(dataframe['Alt'], dataframe['U'], 8)
    y__curve = np.linspace(dataframe['Alt'].min(), dataframe['Alt'].max(), len(dataframe))
    x__curve = np.polyval(coeff, y__curve)
    dataframe['UP'] = dataframe['U'] - x__curve

    coeff = np.polyfit(dataframe['Alt'], dataframe['V'], 8)
    x__curve = np.polyval(coeff, y__curve)
    dataframe['VP'] = dataframe['V'] - x__curve

def calcTempPert(dataframe):
    """
    @param dataframe:
    @return:
    """
    coeff = np.polyfit(dataframe['Alt'], dataframe['T'], 6)
    y__curve = np.linspace(dataframe['Alt'].min(), dataframe['Alt'].max(), len(dataframe))
    x__curve = np.polyval(coeff, y__curve)
    dataframe['Temp_Pert'] = dataframe['T'] - x__curve


def generate_profile_data(path_name):
    """
    @param path_name:
    @return:
    """

    head_data_start_line, head_data_end_line = headerData(path_name)
    data_start_line, data_end_line = grabProfileData(path_name)
    if head_data_start_line is not None and head_data_end_line is not None:
        nrows_to_read = head_data_end_line - head_data_start_line
        header_df = pd.read_csv(path_name, sep='\t', skiprows=head_data_start_line, nrows=nrows_to_read, engine='python',
                                encoding='ISO-8859-1', header=None)

    if head_data_start_line is None and head_data_end_line is None:
        profile_df = pd.read_csv(path_name, sep='\t', engine='python',
                                 encoding='ISO-8859-1')
        profile_df['Time'] = profile_df.index
        profile_df.rename(columns=lambda x: x.strip(), inplace=True)
        profile_df = profile_df[~(profile_df == -999.9).any(axis=1)]
        profile_df = profile_df.rename(columns={"Lat": "Lat.", "Long": "Long.", })

    else:
        if data_start_line is not None and data_end_line is not None:
            nrows_to_read = data_end_line - data_start_line
            profile_df = pd.read_csv(path_name, sep='\t', skiprows=data_start_line, nrows=nrows_to_read, engine='python',
                                     encoding='ISO-8859-1')
            # profile_df.columns += profile_df.iloc[0]
            profile_df.rename(columns=lambda x: x.strip(), inplace=True)
            profile_df = profile_df[1:]
            profile_df = profile_df[['Time', 'P', 'T', 'Hu', 'Ws', 'Wd', 'Long.', 'Lat.', 'Alt', 'Rs']]

        for col in profile_df.select_dtypes(include=['object']).columns:
            profile_df[col] = pd.to_numeric(profile_df[col], errors='coerce')
            profile_df[col] = profile_df[col].astype(float)


    # Calculates the difference between followings alts
    profile_df['Alt_diff'] = profile_df['Alt'].diff()
    profile_df['Time_diff'] = profile_df["Time"].diff()
    peak_index = profile_df[profile_df['Alt_diff'] < 0].first_valid_index()

    # Drop rows after peak and drop diff column
    if peak_index is not None:
        profile_df = profile_df.loc[:peak_index - 1]

    profile_df['Ascending_Rate'] = profile_df['Alt_diff'] / profile_df['Time_diff']
    #grab tropopause value
    Tropopause = (get_tropopause_value(path_name,profile_df))
    if Tropopause is None:
        raise utils.MalformedFileError

    #calculate wind computations and temperature pertubation
    calcWindComps(profile_df)
    calcTempPert(profile_df)
    profile_df['Log_P'] = np.log(profile_df['P'])
    closest_index = (profile_df['P'] - Tropopause).abs().idxmin()

    #create troposphere and stratosphere dataframes to be graphed
    tropo_df = profile_df.iloc[:closest_index + 1]
    strato_df = profile_df.iloc[closest_index + 1:]


    station = Station(path_name, profile_df, strato_df, tropo_df)
    return station
