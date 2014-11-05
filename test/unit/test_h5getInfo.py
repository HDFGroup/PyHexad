# Standard library imports
import logging
import os
import unittest

# Third-party imports
import h5py

# Local imports
from pyhexad.h5getInfo import render_info
from .config import TEST_FILES_DIRECTORY

logger = logging.getLogger(__name__)

def get_test_file(name):
    """ Return the absolute path to the given test file. """
    return os.path.join(TEST_FILES_DIRECTORY, name)

class H5getInfoTest(unittest.TestCase):

    def test_render_info_tickdata(self):
        file_name = get_test_file('cadchftickdata.h5')

        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 8)

            lst = render_info(loc, '/18-09-2011')
            self.assertEqual(len(lst), 3)

            with self.assertRaises(TypeError):
                render_info('Hello World')

    def test_render_info_compound_data(self):
        file_name = get_test_file('compound.h5')

        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 5)

    def test3(self):
        file_name = get_test_file('compound_attr.h5')

        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 3)

    def test4(self):
        file_name = get_test_file('empty.h5')

        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 1)

    def test5(self):
        file_name = get_test_file('group100.h5')

        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 102)

    def test6(self):
        file_name = get_test_file('hdfeos5.h5')

        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 4)

    def test7(self):
        file_name = get_test_file('namedtype.h5')

        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 4)
            lst = render_info(loc, 'dtype_simple')
            self.assertEqual(len(lst), 3)

    def test8(self):
        file_name = get_test_file('tall.h5')

        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 7)
            lst = render_info(loc, '/g1/g1.2/g1.2.1')
            self.assertEqual(len(lst), 3)
            lst = render_info(loc, '/g1/g1.2/g1.2.1/slink')
            self.assertEqual(len(lst), 2)

    def test9(self):
        file_name = get_test_file('tall_with_udlink.h5')

        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 7)
            lst = render_info(loc, '/g1/g1.2/extlink')
            self.assertEqual(len(lst), 2)
            self.assertRaises(Exception, render_info, loc, '/g2/udlink')

    def test10(self):
        file_name = get_test_file('tgroup.h5')

        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 5)

    def test11(self):
        file_name = get_test_file('tref.h5')

        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 4)

    def test12(self):
        file_name = get_test_file('tstr.h5')

        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 7)

    def test13(self):
        file_name = get_test_file('zerodim.h5')

        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 3)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    #setup test files
    unittest.main()
