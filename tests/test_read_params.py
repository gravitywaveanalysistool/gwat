import os.path
import unittest
from src import utils
import shutil


class TestReadParams(unittest.TestCase):
    def test_good_data(self):
        """
        Test to ensure utils.get_parameter_file() will correctly read a properly formatted file
        """
        shutil.copy('./tests/data/params_gooddata.txt', utils.get_parameter_file())

        def cleanup():
            if os.path.isfile(utils.get_parameter_file()):
                os.remove(utils.get_parameter_file())

        self.addCleanup(cleanup)

        tropo_params, strato_params = utils.read_params()

        expected_tropo_dict = {
            "Horizontal Wavelength": 32.450845,
            "Vertical Wavelength": 1.98727,
            "Mean Phase Propogation Direction": 284.34755,
            "Upward Propogation Fraction": 56.9537,
            "Zonal Momentum Flux": -0.13523987,
            "Meridional Momentum Flux": 0.034591745,
            "Potential Energy": 27.121776,
            "Kinetic Energy": 5.2096564,
        }
        expected_strato_dict = {
            "Horizontal Wavelength": 400.51650,
            "Vertical Wavelength": 1.37596,
            "Mean Phase Propogation Direction": 263.92208,
            "Upward Propogation Fraction": 81.0348,
            "Zonal Momentum Flux": -0.0048585038,
            "Meridional Momentum Flux": -0.00051733124,
            "Potential Energy": 1.5404905,
            "Kinetic Energy": 4.2649909,
        }

        self.assertEqual(len(expected_tropo_dict), len(tropo_params))
        self.assertEqual(len(expected_strato_dict), len(strato_params))

        for (key, value) in expected_tropo_dict.items():
            v = float(tropo_params[key])
            self.assertAlmostEqual(v, value)

        for (key, value) in expected_strato_dict.items():
            v = float(strato_params[key])
            self.assertAlmostEqual(v, value)

    def test_bad_data(self):
        """
        Test to ensure utils.get_parameter_file will raise a MalformedFileError if the provided file is incorrectly
        formatted
        """
        shutil.copy('tests/data/params_baddata.txt', utils.get_parameter_file())

        def cleanup():
            if os.path.isfile(utils.get_parameter_file()):
                os.remove(utils.get_parameter_file())

        self.addCleanup(cleanup)

        self.assertRaises(utils.MalformedFileError, utils.read_params)

    def test_no_file(self):
        """
        Test to ensure utils.get_parameter_file will raise a FileNotFound error if there is no file in the expected
        location
        """
        if os.path.isfile(utils.get_parameter_file()):
            os.remove(utils.get_parameter_file())

        self.assertRaises(FileNotFoundError, utils.read_params)


if __name__ == '__main__':
    unittest.main()
