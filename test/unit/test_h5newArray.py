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
from pyhexad.h5newArray import new_array
from .config import TEST_FILES_DIRECTORY

logger = logging.getLogger(__name__)

def get_test_file(name):
    """ Return the absolute path to the given test file. """
    return os.path.join(TEST_FILES_DIRECTORY, name)

def get_temp_file():
    """ Return the absolute path to a temp file. """
    return tempfile.mktemp('.h5')

class H5newArrayTest(unittest.TestCase):

    def test_new_array(self):
        file_name = get_temp_file()

        with h5py.File(file_name) as loc:
            
            # vanilla

            path = '/A'
            size = [[12,13]]
            msg = new_array(loc, path, size)
            self.assertEqual(msg, path)

            path = '/AA'
            size = [[12,13]]
            plist = 'Datatype,uint8'
            msg = new_array(loc, path, size, plist)
            self.assertEqual(msg, path)

            path = '/B'
            size = [[12], [13], [14]]
            plist = 'Datatype,int32'
            msg = new_array(loc, path, size, plist)
            self.assertEqual(msg, path)

            path = '/C/D'
            size = [[12, -16]]
            plist = 'Datatype,single'
            msg = new_array(loc, path, size, plist)
            self.assertEqual(msg, path)

            path = '/E/F'
            size = [[12, -16]]
            plist = 'Datatype,single,Chunksize,[4 4]'
            msg = new_array(loc, path, size, plist)
            self.assertEqual(msg, path)

            path = '/AAA/FF'
            size = [[-12]]
            plist = 'Datatype,single,Chunksize,[3]'
            msg = new_array(loc, path, size, plist)
            self.assertEqual(msg, path)

            path = '/E/F (gzipped)'
            size = [[12, -16]]
            plist = 'Datatype,single,ChunksIZe,[4   4],Deflate,  6'
            msg = new_array(loc, path, size, plist)
            self.assertEqual(msg, path)

            path = '/E/F (gzipped + checksums)'
            size = [[126, -44]]
            plist = 'Datatype,single,Chunksize,[4 4],Deflate,6,Fletcher32,true'
            msg = new_array(loc, path, size, plist)
            self.assertEqual(msg, path)

            path = '/E/F (filled)'
            size = [[126, -44]]
            plist = 'DataType,Single,FillValue,1.2345'
            msg = new_array(loc, path, size, plist)
            self.assertEqual(msg, path)

            path = '/E/F (int filled)'
            size = [[126, -44]]
            plist = 'datatype,uint16,FillValue,123'
            msg = new_array(loc, path, size, plist)
            self.assertEqual(msg, path)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    #setup test files
    unittest.main()
