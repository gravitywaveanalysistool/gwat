import unittest
from src import utils
from src import runGDL
from src import parseradfile
from tests import test_run_gdl


class TestCreateGDLFile(unittest.TestCase):
    def test_doesnt_screw_up_artemis(self):
        """
        Test to ensure file created by create_gdl_friendly_profile yields the same parameters as normally run profile
        """
        gdl_or_idl, outfile = test_run_gdl.gdl_preamble(self)
        self.addCleanup(test_run_gdl.gdl_cleanup)

        input_path = './tests/data/gdl_gooddata.txt'

        runGDL.run_gdl(input_path, -35, gdl_or_idl)
        ref_tropo, ref_strato = utils.read_params()

        station = parseradfile.generate_profile_data(input_path)
        filepath = runGDL.create_gdl_friendly_file(station.profile_df)
        runGDL.run_gdl(filepath, -35, gdl_or_idl)
        test_tropo, test_strato = utils.read_params()

        print(ref_tropo, test_tropo)
        print(ref_strato, test_strato)

        for param, _ in ref_tropo.items():
            ref_p = float(ref_tropo[param])
            test_p = float(test_tropo[param])
            self.assertAlmostEqual(ref_p, test_p)

        for param, _ in ref_strato.items():
            ref_p = float(ref_strato[param])
            test_p = float(test_strato[param])
            self.assertAlmostEqual(ref_p, test_p)

    def test_new_format(self):
        gdl_or_idl, outfile = test_run_gdl.gdl_preamble(self)
        self.addCleanup(test_run_gdl.gdl_cleanup)

        input_path = './tests/data/newformat.txt'

        station = parseradfile.generate_profile_data(input_path)
        filepath = runGDL.create_gdl_friendly_file(station.profile_df)
        runGDL.run_gdl(filepath, -35, gdl_or_idl)
        tropo, strato = utils.read_params()

if __name__ == '__main__':
    unittest.main()
