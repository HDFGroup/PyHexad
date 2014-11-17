# Standard library imports
import logging
import math
import os
from os.path import isfile
import tempfile
import unittest

# Third-party imports
import h5py
import numpy as np

# Local imports
from pyhexad.h5appendRows import append_rows
from pyhexad.h5newTable import new_table
from .config import TEST_FILES_DIRECTORY

logger = logging.getLogger(__name__)

def get_test_file(name):
    """ Return the absolute path to the given test file. """
    return os.path.join(TEST_FILES_DIRECTORY, name)

def get_temp_file():
    """ Return the absolute path to a temp file. """
    return tempfile.mktemp('.h5')

class H5appendRowsTest(unittest.TestCase):

    def test_single_column_table(self):
        file_name = get_temp_file()

        with h5py.File(file_name) as loc:
            
            path = '/A/B/C'
            heading = 'City\, State,uint8'
            msg = new_table(loc, path, heading)
            self.assertEqual(msg, path)

            count = 256
            l = []
            for i in range(count):
                l.append([i])

            msg = append_rows(loc, path, l)
            self.assertEqual(msg, '%d rows appended.' % (count)) 
            msg = append_rows(loc, path, l)
            self.assertEqual(msg, '%d rows appended.' % (count)) 
            
    def test_multi_column_table(self):
        file_name = get_temp_file()

        with h5py.File(file_name) as loc:
            
            path = '/F'
            heading = 'Howdy,string,x,double,y,single,v,int'
            msg = new_table(loc, path, heading)
            self.assertEqual(msg, path)

            count = 1024
            l = []
            for i in range(count):
                l.append(['Hello, World!', math.pi, math.e, i])
            
            print file_name            
            msg = append_rows(loc, path, l)
            self.assertEqual(msg, '%d rows appended.' % (count)) 
            msg = append_rows(loc, path, l)
            self.assertEqual(msg, '%d rows appended.' % (count)) 


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    #setup test files
    unittest.main()
