# Standard library imports
import logging
import os
from os.path import isfile
import shutil
import stat
import unittest

# Third-party imports
import h5py
import numpy as np

# Local imports
from pyhexad.h5readTable import get_table
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

class H5readTableTest(unittest.TestCase):

    def test_full_table(self):
        
        file_name = get_test_file('cadchftickdata.h5')

        with h5py.File(file_name) as loc:
            a, msg = get_table(loc, '/22-09-2011')
            self.assertEqual(len(a), 23537)

    def test_column_subset(self):
        
        file_name = get_test_file('cadchftickdata.h5')

        with h5py.File(file_name) as loc:
            a, msg = get_table(loc, '/22-09-2011', [['Time'], ['Ask']])
            self.assertEqual(len(a), 23537)

    def test_single_column(self):
        
        file_name = get_test_file('cadchftickdata.h5')

        with h5py.File(file_name) as loc:
            a, msg = get_table(loc, '/22-09-2011', [['Time']])
            self.assertEqual(len(a), 23537)
            
    def test_row_range(self):
        
        file_name = get_test_file('cadchftickdata.h5')

        with h5py.File(file_name) as loc:
            a, msg = get_table(loc, '/22-09-2011', None, 4711, 10000)
            self.assertEqual(len(a), 5291)

    def test_row_range_sampled(self):
        
        file_name = get_test_file('cadchftickdata.h5')

        with h5py.File(file_name) as loc:
            a, msg = get_table(loc, '/22-09-2011', None, 4711, 10000, 3)
            self.assertEqual(len(a), 1765)
            
    def test_table_sampled(self):
        
        file_name = get_test_file('cadchftickdata.h5')

        with h5py.File(file_name) as loc:
            a, msg = get_table(loc, '/22-09-2011', None, None, None, 10)
            self.assertEqual(len(a), 2355)

    def test_column_subset_row_range(self):
        
        file_name = get_test_file('cadchftickdata.h5')

        with h5py.File(file_name) as loc:
            a, msg = get_table(loc, '/22-09-2011', [['Time'], ['Ask']], 444, 12345)
            self.assertEqual(len(a), 11903)
            
    def test_column_subset_sampled(self):
        
        file_name = get_test_file('cadchftickdata.h5')

        with h5py.File(file_name) as loc:
            a, msg = get_table(loc, '/22-09-2011', [['Time'], ['Ask']], None, None, 10)
            self.assertEqual(len(a), 2355)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    #setup test files
    unittest.main()
