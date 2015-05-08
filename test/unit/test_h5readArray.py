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
import unittest

# Third-party imports
import h5py
import numpy as np

# Local imports
from pyhexad.h5readArray import get_ndarray
from .config import TEST_FILES_DIRECTORY

logger = logging.getLogger(__name__)

def get_test_file(name):
    """ Return the absolute path to the given test file. """
    return os.path.join(TEST_FILES_DIRECTORY, name)

class H5readArrayTest(unittest.TestCase):

    def testScalar(self):
        
        file_name = get_test_file('hdfeos5.h5')

        with h5py.File(file_name) as loc:
            a, msg = get_ndarray(loc, \
                                 '/HDFEOS INFORMATION/coremetadata.0')
            self.assertEqual(msg, '1 x 1')
            self.assertEqual(len(a[0]), 33032)
    
    def test1D(self):
        
        file_name = get_test_file('hdfeos5.h5')

        with h5py.File(file_name) as loc:
            a, msg = get_ndarray(
                loc, '/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Latitude')
            self.assertEqual(a.size, 5554)

            a, msg = get_ndarray(
                loc, '/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Latitude',
                np.asarray((10,)))
            self.assertEqual(a.size, 5545)

            a, msg = get_ndarray(
                loc, '/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Latitude',
                np.asarray((10,)), np.asarray((20,)))
            self.assertEqual(a.size, 11)

            a, msg = get_ndarray(
                loc, '/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Latitude',
                np.asarray((10,)), np.asarray((20,)), np.asarray((2,)))
            self.assertEqual(a.size, 6)

            a, msg = get_ndarray(
                loc, '/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Latitude',
                None, np.asarray((20,)), np.asarray((19,)))
            self.assertEqual(a.size, 2)

            a, msg = get_ndarray(
                loc, '/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Latitude',
                np.asarray((20,)), None, np.asarray((19,)))
            self.assertEqual(a.size, 292)

            a, msg = get_ndarray(
                loc, '/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Latitude',
                None, None, np.asarray((10,)))
            self.assertEqual(a.size, 556)

    def test2D(self):
        
        file_name = get_test_file('hdfeos5.h5')

        with h5py.File(file_name) as loc:
            a, msg = get_ndarray(
                loc, '/HDFEOS/SWATHS/HIRDLS/Data Fields/O3')
            self.assertEqual(a.shape[0], 5554)
            self.assertEqual(a.shape[1], 145)

            a, msg = get_ndarray(
                loc, '/HDFEOS/SWATHS/HIRDLS/Data Fields/O3',
                np.asarray((10,20)))
            self.assertEqual(a.shape[0], 5545)
            self.assertEqual(a.shape[1], 126)

            a, msg = get_ndarray(
                loc, '/HDFEOS/SWATHS/HIRDLS/Data Fields/O3',
                np.asarray((10,20)), np.asarray((15,26)))
            self.assertEqual(a.shape[0], 6)
            self.assertEqual(a.shape[1], 7)

            a, msg = get_ndarray(
                loc, '/HDFEOS/SWATHS/HIRDLS/Data Fields/O3',
                np.asarray((10,20)), np.asarray((15,26)), np.asarray((2,3)))
            self.assertEqual(a.shape[0], 3)
            self.assertEqual(a.shape[1], 3)

            a, msg = get_ndarray(
                loc, '/HDFEOS/SWATHS/HIRDLS/Data Fields/O3',
                None, np.asarray((15,26)), np.asarray((2,3)))
            self.assertEqual(a.shape[0], 8)
            self.assertEqual(a.shape[1], 9)

            a, msg = get_ndarray(
                loc, '/HDFEOS/SWATHS/HIRDLS/Data Fields/O3',
                np.asarray((10,20)), None, np.asarray((2,3)))
            self.assertEqual(a.shape[0], 2773)
            self.assertEqual(a.shape[1], 42)

            a, msg = get_ndarray(
                loc, '/HDFEOS/SWATHS/HIRDLS/Data Fields/O3',
                None, None, np.asarray((2,3)))
            self.assertEqual(a.shape[0], 2777)
            self.assertEqual(a.shape[1], 49)

            a, msg = get_ndarray(
                loc, '/HDFEOS/SWATHS/HIRDLS/Data Fields/O3',
                np.asarray((1,1)), np.asarray((1,1)), None)
            self.assertEqual(a.shape[0], 1)
            self.assertEqual(a.shape[1], 1)

            a, msg = get_ndarray(
                loc, '/HDFEOS/SWATHS/HIRDLS/Data Fields/O3',
                np.asarray((0,0)), np.asarray((1,1)), None)
            self.assertEqual(a, None)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    #setup test files
    unittest.main()
