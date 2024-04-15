import os.path
import unittest
from src import runGDL
from src import utils


class TestRunGDL(unittest.TestCase):

    def gdl_preamble(self):
        gdl_or_idl = runGDL.detect_gdl_idl()
        self.assertNotEqual(gdl_or_idl, 'none', 'gdl/idl not installed')

        outfile = utils.get_parameter_file()
        if os.path.isfile(outfile):
            os.remove(outfile)

        return gdl_or_idl, outfile

    def gdl_cleanup(self):
        if os.path.isfile(utils.get_parameter_file()):
            os.remove(utils.get_parameter_file())

    def test_good_data(self):
        gdl_or_idl, outfile = self.gdl_preamble()

        runGDL.runGDL('./tests/data/gdl_gooddata.txt', -35, gdl_or_idl)

        self.assertTrue(os.path.isfile(outfile))

        gw = open(outfile, 'r')
        self.addCleanup(gw.close)

        params = [32.450845, 1.98727, 284.34755, 56.9537, -0.13523987, 0.034591745, 27.121776, 5.2096564, 400.51650,
                  1.37596, 263.92208, 81.0348, -0.0048585038, -0.00051733124, 1.5404905, 4.2649909, ]

        for p in params:
            v = float(gw.readline().strip())
            self.assertAlmostEqual(v, p)
        
        gw.close()

        os.remove(outfile)

    def test_bad_data(self):
        gdl_or_idl, outfile = self.gdl_preamble()
        self.addCleanup(self.gdl_cleanup)

        self.assertRaises(runGDL.GDLError, runGDL.runGDL, './tests/data/gdl_baddata.txt', -35, gdl_or_idl)

        self.assertFalse(os.path.isfile(outfile))

    def test_no_file(self):
        gdl_or_idl, outfile = self.gdl_preamble()
        self.addCleanup(self.gdl_cleanup)

        self.assertRaises(FileNotFoundError, runGDL.runGDL, '..', -35, gdl_or_idl)

        self.assertFalse(os.path.isfile(outfile))


if __name__ == '__main__':
    unittest.main()
