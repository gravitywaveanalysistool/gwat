from src.utils import save_params_to_file, get_temp_folder
import unittest
import os


def generate_tropo():
    tropo_params = {"Horizontal Wavelength": "32.45", "Vertical Wavelength": "1.987",
                   "Mean Phase Propogation Direction": "284.34",
                   "Upward Propogation Fraction": "56.95",
                   "Zonal Momentum Flux": "-0.135", "Meridional Momentum Flux": "0.0345", "Potential Energy": "27.12",
                   "Kinetic Energy": "5.21"}
    return tropo_params


def generate_strato():
    strato_params = {"Horizontal Wavelength": 400.51, "Vertical Wavelength": 1.375,
                    "Mean Phase Propogation Direction": 263.92,
                    "Upward Propogation Fraction": 81.03,
                    "Zonal Momentum Flux": -0.004, "Meridional Momentum Flux": -0.0005, "Potential Energy": 1.54,
                    "Kinetic Energy": 4.26}
    return strato_params


def cleanup(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)


class TestSaveParamsToFile(unittest.TestCase):

    def test_good_path(self):
        """
        Test to ensure a correctly formatted file will be generated
        """

        strato_params, tropo_params = generate_strato(), generate_tropo()

        file_path = get_temp_folder() + "params.txt"

        self.addCleanup(lambda: cleanup(file_path))

        save_params_to_file(strato_params, tropo_params, file_path)

        # Checks if the file exists
        self.assertTrue(os.path.exists(file_path))

        def contains_line(params):
            for i, (key, val) in enumerate(params.items()):
                if (key + " " + str(val)).split() == line.split():
                    return True
            return False

        # Validates the contents of the file
        f = open(file_path, "r")
        current_layer = "none"
        for line in f:
            if line.strip() == "Stratosphere:" or line.strip() == "Troposphere:":
                current_layer = line.strip()
            else:
                # ensure there is content in the line
                if line.strip():
                    # ensure the content of the line is found in the correct dictionary
                    self.assertTrue(contains_line(strato_params if current_layer == "Stratosphere:" else tropo_params))

        f.close()

    def test_bad_path(self):
        """
        Make sure that if the output filepath does not exist/is not valid to cancel execution and alert the user
        """
        strato_params, tropo_params = generate_strato(), generate_tropo()

        file_path = ".."

        self.addCleanup(lambda: cleanup(file_path))

        self.assertRaises(Exception, lambda: save_params_to_file(strato_params, tropo_params, file_path))


if __name__ == '__main__':
    unittest.main()

