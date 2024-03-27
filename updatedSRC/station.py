import pandas as pd


class Station:

    def __init__(self, file_path, profile_df, tropo_df, header_df):
        """
        Initializes a Station instance.

        Args:
            file_path (str): The file path of the station data.
            profile_df (pandas.DataFrame): The DataFrame containing profile data.
            tropo_df (pandas.DataFrame): The DataFrame containing tropo data.
            header_df (pandas.DataFrame): The DataFrame containing header data.
        """
        self.file_path = file_path
        self.profile_df = profile_df.copy()
        self.tropo_df = tropo_df.copy()
        self.header_df = header_df.copy()
        self.station_name = str(self.header_df.at[1, 3])
        #self.gdl_params_df = gld_params_df.copy()

