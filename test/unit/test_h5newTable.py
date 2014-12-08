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
import os
from os.path import isfile
import tempfile
import unittest

# Third-party imports
import h5py

# Local imports
from pyhexad.h5newTable import new_table
from .config import TEST_FILES_DIRECTORY

logger = logging.getLogger(__name__)

def get_test_file(name):
    """ Return the absolute path to the given test file. """
    return os.path.join(TEST_FILES_DIRECTORY, name)

def get_temp_file():
    """ Return the absolute path to a temp file. """
    return tempfile.mktemp('.h5')

class H5newTableTest(unittest.TestCase):

    def test_new_table(self):
        file_name = get_temp_file()

        with h5py.File(file_name) as loc:
            
            path = '/A'
            heading = 'City\, State,uint8'
            msg = new_table(loc, path, heading)
            self.assertEqual(msg, path)
            
            path = '/B/C'
            heading = 'City\, State,uint8,x,double,y,double,A\, B,int16,v,single[2]'
            msg = new_table(loc, path, heading)
            self.assertEqual(msg, path)
            
            path = '/E'
            heading = 'Howdy,uint8,x,double,y,double,v,single[3 3]'
            msg = new_table(loc, path, heading)
            self.assertEqual(msg, path)
            
            path = '/F'
            heading = 'Howdy,string,x,double,y,double,v,single[3]'
            msg = new_table(loc, path, heading)
            self.assertEqual(msg, path)
            
            path = '/G'
            heading = 'Howdy,string,x,double,y,double,v,single[3]'
            plist = 'Deflate,6,Fletcher32,true'
            msg = new_table(loc, path, heading, plist)
            self.assertEqual(msg, path)

            path = '/H'
            heading = 'Howdy,string,x,double,y,double,v,single[3]'
            plist = 'Chunksize,128,Deflate,6,Fletcher32,true'
            msg = new_table(loc, path, heading, plist)
            self.assertEqual(msg, path)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    #setup test files
    unittest.main()
