import unittest
from src.parseradfile import headerData, grabProfileData, calc_tropopause, generate_profile_data, get_latitude_value
import pandas as pd
import src.utils as utils

class TestRadiosondeDataProcessing(unittest.TestCase):
    def setUp(self):
        # This is the path to a test file. Adjust it according to your test data directory.
        #self.test_file_path = './data/NewYork_SUNYOswego_231013_1642_Q3.txt'
        self.test_file_path = './data/T3_1800_12132020_Artemis_Rerun.txt'

    def test_headerData(self):
        # Test the function with expected headers
        start_line, end_line = headerData(self.test_file_path)
        self.assertIsNotNone(start_line)
        self.assertIsNotNone(end_line)
        #uncomment for the other format
        #self.assertIsInstance(start_line, int)
        #self.assertIsInstance(end_line, int)

    def test_grabProfileData(self):
        start_line, end_line = grabProfileData(self.test_file_path)
        #uncomment for the other format
        #self.assertIsNotNone(start_line)
        #self.assertIsNotNone(end_line)
        self.assertIsInstance(start_line, int)
        self.assertIsInstance(end_line, int)

    def test_calc_tropopause(self):
        data = {'Alt': [1000, 2000, 3000, 4000], 'T': [20, 15, 14, 5], 'P': [1000, 800, 600, 400]}
        #data = {'Alt': [1000, 2000, 3000, 4000], 'T': [20, 15, 10, 5]}
        df = pd.DataFrame(data)
        tropopause_pressure = calc_tropopause(df, 1000)
        self.assertIsInstance(tropopause_pressure, float)

    def test_get_latitude(self):
        alaskaFormat = get_latitude_value("./data/Alaska_UAF_231013_1704_Q2.txt")
        headerFormat = get_latitude_value("./data/T3_1800_12132020_Artemis_Rerun.txt")
        oswegoFormat = get_latitude_value("./data/SUO011800_040724_id1.txt")
        self.assertIsNotNone(alaskaFormat)
        self.assertIsNotNone(headerFormat)
        self.assertIsNotNone(oswegoFormat)



    #test generate profile data formats
    def test_generate_profile_data(self):
        #should return no tropopause
        headerFormat = generate_profile_data("./data/T3_1800_12132020_Artemis_Rerun.txt")
        nonHeaderFormat = generate_profile_data("./data/Alaska_UAF_231013_2100_Q2.txt")
        self.assertRaises(utils.MalformedFileError,generate_profile_data,"./data/Alaska_UAF_231013_1704_Q2.txt")
        self.assertIsNotNone(headerFormat)
        self.assertIsNotNone(nonHeaderFormat)

if __name__ == '__main__':
    unittest.main()