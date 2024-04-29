import pandas as pd


class Station:

    def __init__(self, file_path, profile_df, strato_df, tropo_df):
        """
        Initializes a Station instance.

        Args:
            file_path (str): The file path of the station data.
            profile_df (pandas.DataFrame): The DataFrame containing profile data.
            tropo_df (pandas.DataFrame): The DataFrame containing tropo data.
        """
        self.file_path = file_path
        self.profile_df = profile_df.copy()
        self.strato_df = strato_df.copy()
        self.tropo_df = tropo_df.copy()

