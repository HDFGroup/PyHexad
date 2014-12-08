##############################################################################
# Copyright by The HDF Group.                                                #
# All rights reserved.                                                       #
#                                                                            #
# This file is part of PyHexad. The full PyHexad copyright notice, including #
# terms governing use, modification, and redistribution, is contained in     #
# the file COPYING, which can be found at the root of the source code        #
# distribution tree.  If you do not have access to this file, you may        #
# request a copy from help@hdfgroup.org.                                     #
##############################################################################

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
from pyhexad.h5newTable import new_table
from pyhexad.h5writeTable import write_rows
from .config import TEST_FILES_DIRECTORY

logger = logging.getLogger(__name__)

def get_test_file(name):
    """ Return the absolute path to the given test file. """
    return os.path.join(TEST_FILES_DIRECTORY, name)

def get_temp_file():
    """ Return the absolute path to a temp file. """
    return tempfile.mktemp('.h5')

class H5writeTableTest(unittest.TestCase):

    def test_single_column_table(self):
        file_name = get_temp_file()

        with h5py.File(file_name) as loc:
            
            path = '/A/B/C'
            heading = 'City\, State,uint16'
            msg = new_table(loc, path, heading)
            self.assertEqual(msg, path)

            count = 256
            l = []
            for i in range(count):
                l.append([i])

            msg = write_rows(loc, path, l, '')
            self.assertEqual(msg, '%d rows written.' % (count))

            # write so that the table needs to be extended
            
            count = 512
            l = []
            for i in range(count):
                l.append([i])

            msg = write_rows(loc, path, l, 'City\, State')
            self.assertEqual(msg, '%d rows written.' % (count)) 
            
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
            
            msg = write_rows(loc, path, l, '')
            self.assertEqual(msg, '%d rows written.' % (count))

            # write a subset of columns and rows
            
            count = 512
            l = []
            for i in range(count):
                l.append(['Hello again, World!', count-i])
            msg = write_rows(loc, path, l, 'Howdy,v')            
            self.assertEqual(msg, '%d rows written.' % (count)) 


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    #setup test files
    unittest.main()
