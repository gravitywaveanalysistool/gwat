import os.path
import unittest
from src import runGDL
from src import utils


def gdl_preamble(test_case):
    gdl_or_idl = runGDL.detect_gdl_idl()
    test_case.assertNotEqual(gdl_or_idl, 'none', 'gdl/idl not installed')

    outfile = utils.get_parameter_file()
    if os.path.isfile(outfile):
        os.remove(outfile)

    return gdl_or_idl, outfile


def gdl_cleanup():
    if os.path.isfile(utils.get_parameter_file()):
        os.remove(utils.get_parameter_file())


class TestRunGDL(unittest.TestCase):
    def test_good_data(self):
        """
        Test to ensure runGDL will produce a correct results file when provided correctly formatted, error free data
        """
        gdl_or_idl, outfile = gdl_preamble(self)

        runGDL.run_gdl('./tests/data/gdl_gooddata.txt', -35, gdl_or_idl)

        self.assertTrue(os.path.isfile(outfile))
        self.addCleanup(gdl_cleanup)

        gw = open(outfile, 'r')
        self.addCleanup(gw.close)

        params = [32.450845, 1.98727, 284.34755, 56.9537, -0.13523987, 0.034591745, 27.121776, 5.2096564, 400.51650,
                  1.37596, 263.92208, 81.0348, -0.0048585038, -0.00051733124, 1.5404905, 4.2649909, ]

        for p in params:
            v = float(gw.readline().strip())
            self.assertAlmostEqual(v, p, places=3)

    def test_bad_data(self):
        """
        Test to insure runGDL will raise a GDLError if provided incorrectly formatted data
        """
        gdl_or_idl, outfile = gdl_preamble(self)
        self.addCleanup(gdl_cleanup)

        self.assertRaises(runGDL.GDLError, runGDL.run_gdl, './tests/data/gdl_baddata.txt', -35, gdl_or_idl)

        self.assertFalse(os.path.isfile(outfile))

    def test_no_file(self):
        """
        Test to ensure runGDL will raise a FileNotFound error if provided with an invalid file path
        """
        gdl_or_idl, outfile = gdl_preamble(self)
        self.addCleanup(gdl_cleanup)

        self.assertRaises(FileNotFoundError, runGDL.run_gdl, '..', -35, gdl_or_idl)

        self.assertFalse(os.path.isfile(outfile))


if __name__ == '__main__':
    unittest.main()
