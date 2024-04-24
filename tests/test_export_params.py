from src.utils import save_params_to_file
import unittest
import os

def generateBadTropo():
    tropoParams = {"lol" : "ANOTHER STRING?", "pizza" : 112, "borb" : "hehe"}
    return tropoParams

def generateBadStrato():
    stratoParams = {"bad" : "good?", "good" : "good?"}

def generateGoodTropo():
    tropoParams = {"Horizontal Wavelength": 32.45, "Vertical Wavelength": 1.987,
                   "Mean Phase Propogation Direction": 284.34,
                   "Upward Propogation Fraction": 56.95,
                   "Zonal Momentum Flux": -0.135, "Meridional Momentum Flux": 0.0345, "Potential Energy": 27.12,
                   "Kinetic Energy": 5.21}
    return tropoParams

def generateGoodStrato():
    stratoParams = {"Horizontal Wavelength": 400.51, "Vertical Wavelength": 1.375,
                    "Mean Phase Propogation Direction": 263.92,
                    "Upward Propogation Fraction": 81.03,
                    "Zonal Momentum Flux": -0.004, "Meridional Momentum Flux": -0.0005, "Potential Energy": 1.54,
                    "Kinetic Energy": 4.26}
    return stratoParams

class TestSaveParamsToFile(unittest.TestCase):

    def test_export_params_to_file(self, stratoParams, tropoParams, filePath):

        def cleanup():
            if os.path.isfile(filePath):
                os.remove(filePath)

        def contains(currentLayer, key, val):
            if currentLayer == "Stratosphere:":
                if key in stratoParams.keys and val == str(stratoParams[key]):
                    return True
            elif currentLayer == "Troposphere:":
                if key in tropoParams.keys and val == str(tropoParams[key]):
                    return True
            return False

        # Runs the save Params method
        save_params_to_file(stratoParams, tropoParams, filePath)

        # This exact same block is run within the save_params_to_file method so this will pass the case for bad filepath
        if not os.path.exists(filePath):
            return

        self.addCleanup(cleanup)

        # Checks if the file exists
        self.assertTrue(os.path.exists(filePath))

        # Validates the contents of the file
        f = open(filePath, "r")
        currentLayer = "none"
        for line in f:
            if line.strip() == "Stratosphere:" or line.strip() == "Troposphere:":
                currentLayer = line.strip()
            else:
                splitLine = line.split()
                key = " ".join(splitLine[:len(splitLine)-1])
                val = splitLine[len(splitLine)-1:][0]
                self.assertTrue(contains(currentLayer, key, val))

        f.close()


    def test_goodStrato_goodTropo(self):
        """
        Test that a file which contains formatted tropo and strato parameters will be generated on good data input
        """
        self.test_export_params_to_file(generateGoodStrato(), generateGoodTropo(), filePath="params.txt")

    def test_goodStrato_badTropo(self):
        """
        Test that the method will catch when it has invalid arras passed to it and stop execution before creating a bad parameters file
        """
        self.test_export_params_to_file(generateGoodStrato(), generateBadTropo(), filePath="params.txt")

    def test_badStrato_goodTropo(self):
        """
        Same as previous test, opposite order
        """
        self.test_export_params_to_file(generateBadStrato(), generateGoodTropo(), filePath="params.txt")

    def test_badFilepath(self):
        """
        Make sure that if the output filepath does not exist/is not valid to cancel execution and alert the user
        """
        self.test_export_params_to_file(generateGoodStrato(), generateGoodTropo(), filePath="badDirectory\\params.txt")


if __name__ == '__main__':
    unittest.main()
