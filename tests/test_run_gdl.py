import os.path
import unittest
from src import runGDL
from src import utils


def gdl_preamble():
    gdl_or_idl = runGDL.detect_gdl_idl()
    assert gdl_or_idl != 'none', 'gdl/idl not installed'

    outfile = utils.get_temp_folder() + 'gw_parameters.txt'
    if os.path.isfile(outfile):
        os.remove(outfile)

    return gdl_or_idl, outfile


class TestRunGDL(unittest.TestCase):
    def test_good_data(self):
        gdl_or_idl, outfile = gdl_preamble()

        try:
            runGDL.runGDL('./tests/data/gooddata.txt', -35, gdl_or_idl)
        except Exception as e:
            assert False, e

        assert os.path.isfile(outfile), 'output file was not produced'

        os.remove(outfile)

    def test_bad_data(self):
        gdl_or_idl, outfile = gdl_preamble()

        try:
            runGDL.runGDL('./tests/data/baddata.txt', -35, gdl_or_idl)
        except Exception as e:
            assert e.args[0] == 'gdl_error'

        file_exists = os.path.isfile(outfile)
        # if file_exists:
        #     os.remove(outfile)

        assert not file_exists, 'output file was produced'

    def test_no_file(self):
        gdl_or_idl, outfile = gdl_preamble()

        try:
            runGDL.runGDL('..', -35, gdl_or_idl)
        except Exception as e:
            assert e.args[0] == 'no_file'

        file_exists = os.path.isfile(outfile)
        if file_exists:
            os.remove(outfile)

        assert not file_exists, 'output file was produced'


if __name__ == '__main__':
    unittest.main()
