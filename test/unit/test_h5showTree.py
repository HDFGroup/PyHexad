# Standard library imports
import logging
import os
from os.path import isfile
import shutil
import stat
import unittest

# Third-party imports
import h5py

# Local imports
from pyhexad.h5showTree import render_tree
from .config import TEST_FILES_DIRECTORY

logger = logging.getLogger(__name__)

def get_test_file(name):
    """ Return the absolute path to the given test file. """
    return os.path.join(TEST_FILES_DIRECTORY, name)

# It is not clear what this function does. It does way more than getting a
# file and does not return a file. 
def get_file(name, tgt=None, ro=False):
    src = os.path.join(TEST_FILES_DIRECTORY, name)
    logger.info("copying file to this directory: {}".format(src))
    if not tgt:
        tgt = name
    if isfile(tgt):
        # make sure it's writable, before we copy over it
        os.chmod(tgt, stat.S_IWRITE|stat.S_IREAD)
    shutil.copyfile(src, tgt)
    if ro:
        logger.info('make read-only')
        os.chmod(tgt, stat.S_IREAD)

class H5showTreeTest(unittest.TestCase):

    def test1(self):
        file_name = get_test_file('cadchftickdata.h5')

        with h5py.File(file_name) as loc:
            lst, max_col = render_tree(loc, '/')
            self.assertEqual(len(lst), 7)
            self.assertEqual(max_col, 1)

            lst, max_col = render_tree(loc, '/18-09-2011')
            self.assertEqual(len(lst), 1)
            self.assertEqual(max_col, 1)

            with self.assertRaises(TypeError):
                render_tree('Hello World')

    def test2(self):
        file_name = get_test_file('compound.h5')

        with h5py.File(file_name) as loc:
            lst, max_col = render_tree(loc, '/')
            self.assertEqual(len(lst), 2)
            self.assertEqual(max_col, 1)

    def test3(self):
        file_name = get_test_file('compound_attr.h5')

        with h5py.File(file_name) as loc:
            lst, max_col = render_tree(loc, '/')
            self.assertEqual(len(lst), 1)
            self.assertEqual(max_col, 1)

    def test4(self):
        file_name = get_test_file('empty.h5')

        with h5py.File(file_name) as loc:
            lst, max_col = render_tree(loc, '/')
            self.assertEqual(len(lst), 1)
            self.assertEqual(max_col, 1)

    def test5(self):
        file_name = get_test_file('group100.h5')

        with h5py.File(file_name) as loc:
            lst, max_col = render_tree(loc, '/')
            self.assertEqual(len(lst), 101)
            self.assertEqual(max_col, 1)

    def test6(self):
        file_name = get_test_file('hdfeos5.h5')

        with h5py.File(file_name) as loc:
            lst, max_col = render_tree(loc, '/')
            self.assertEqual(len(lst), 101)
            self.assertEqual(max_col, 5)

    def test7(self):
        file_name = get_test_file('namedtype.h5')

        with h5py.File(file_name) as loc:
            lst, max_col = render_tree(loc, '/')
            self.assertEqual(len(lst), 3)
            self.assertEqual(max_col, 1)

            lst, max_col = render_tree(loc, 'dtype_simple')
            self.assertEqual(len(lst), 1)
            self.assertEqual(max_col, 1)

    def test8(self):
        file_name = get_test_file('tall.h5')

        with h5py.File(file_name) as loc:
            lst, max_col = render_tree(loc, '/')
            self.assertEqual(len(lst), 10)
            self.assertEqual(max_col, 3)

            lst, max_col = render_tree(loc, '/g1/g1.2/g1.2.1')
            self.assertEqual(len(lst), 1)
            self.assertEqual(max_col, 1)

            lst, max_col = render_tree(loc, '/g1/g1.2/g1.2.1/slink')
            self.assertEqual(len(lst), 1)
            self.assertEqual(max_col, 1)

    def test9(self):
        file_name = get_test_file('tall_with_udlink.h5')

        with h5py.File(file_name) as loc:
            lst, max_col = render_tree(loc, '/')
            self.assertEqual(len(lst), 10)
            self.assertEqual(max_col, 3)

            lst, max_col = render_tree(loc, '/g1/g1.2/extlink')
            self.assertEqual(len(lst), 1)
            self.assertEqual(max_col, 1)

            with self.assertRaises(Exception):
                render_tree(loc, '/g2/udlink')

    def test10(self):
        file_name = get_test_file('tgroup.h5')

        with h5py.File(file_name) as loc:
            lst, max_col = render_tree(loc, '/')
            self.assertEqual(len(lst), 14)
            self.assertEqual(max_col, 3)

    def test11(self):
        file_name = get_test_file('tref.h5')

        with h5py.File(file_name) as loc:
            lst, max_col = render_tree(loc, '/')
            self.assertEqual(len(lst), 5)
            self.assertEqual(max_col, 2)

    def test12(self):
        file_name = get_test_file('tstr.h5')

        with h5py.File(file_name) as loc:
            lst, max_col = render_tree(loc, '/')
            self.assertEqual(len(lst), 6)
            self.assertEqual(max_col, 1)

    def test13(self):
        file_name = get_test_file('zerodim.h5')

        with h5py.File(file_name) as loc:
            lst, max_col = render_tree(loc, '/')
            self.assertEqual(len(lst), 2)
            self.assertEqual(max_col, 1)
            
if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    #setup test files
    unittest.main()
