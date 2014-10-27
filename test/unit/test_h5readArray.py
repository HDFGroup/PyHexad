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
from pyhexad.h5readArray import get_ndarray
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

class H5readArrayTest(unittest.TestCase):

    def test1D(self):
        
        file_name = get_test_file('hdfeos5.h5')

        with h5py.File(file_name) as loc:
            a, msg = get_ndarray(loc, \
                                 '/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Latitude')
            self.assertEqual(a.size, 5554)

            a, msg = get_ndarray(loc, \
                                 '/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Latitude', \
                                 np.asarray((10,)))
            self.assertEqual(a.size, 5545)

            a, msg = get_ndarray(loc, \
                                 '/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Latitude', \
                                 np.asarray((10,)), np.asarray((20,)))
            self.assertEqual(a.size, 11)

            a, msg = get_ndarray(loc, \
                                 '/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Latitude', \
                                 np.asarray((10,)), np.asarray((20,)), \
                                 np.asarray((2,)))
            self.assertEqual(a.size, 6)

            a, msg = get_ndarray(loc, \
                                 '/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Latitude', \
                                 None, np.asarray((20,)), np.asarray((19,)))
            self.assertEqual(a.size, 2)

            a, msg = get_ndarray(loc, \
                                 '/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Latitude', \
                                 np.asarray((20,)), None,
                                 np.asarray((19,)))
            self.assertEqual(a.size, 292)

            a, msg = get_ndarray(loc, \
                                 '/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Latitude', \
                                 None, None, np.asarray((10,)))
            self.assertEqual(a.size, 556)

    def test2D(self):
        
        file_name = get_test_file('hdfeos5.h5')

        with h5py.File(file_name) as loc:
            a, msg = get_ndarray(loc, \
                                 '/HDFEOS/SWATHS/HIRDLS/Data Fields/O3')
            self.assertEqual(a.shape[0], 5554)
            self.assertEqual(a.shape[1], 145)

            a, msg = get_ndarray(loc, \
                                 '/HDFEOS/SWATHS/HIRDLS/Data Fields/O3', \
                                 np.asarray((10,20)))
            self.assertEqual(a.shape[0], 5545)
            self.assertEqual(a.shape[1], 126)

            a, msg = get_ndarray(loc, \
                                 '/HDFEOS/SWATHS/HIRDLS/Data Fields/O3', \
                                 np.asarray((10,20)), np.asarray((15,26)))
            self.assertEqual(a.shape[0], 6)
            self.assertEqual(a.shape[1], 7)

            a, msg = get_ndarray(loc, \
                                 '/HDFEOS/SWATHS/HIRDLS/Data Fields/O3', \
                                 np.asarray((10,20)), np.asarray((15,26)), \
                                 np.asarray((2,3)))
            self.assertEqual(a.shape[0], 3)
            self.assertEqual(a.shape[1], 3)

            a, msg = get_ndarray(loc, \
                                 '/HDFEOS/SWATHS/HIRDLS/Data Fields/O3', \
                                 None, np.asarray((15,26)), np.asarray((2,3)))
            self.assertEqual(a.shape[0], 8)
            self.assertEqual(a.shape[1], 9)

            a, msg = get_ndarray(loc, \
                                 '/HDFEOS/SWATHS/HIRDLS/Data Fields/O3', \
                                 np.asarray((10,20)), None, np.asarray((2,3)))
            self.assertEqual(a.shape[0], 2773)
            self.assertEqual(a.shape[1], 42)

            a, msg = get_ndarray(loc, \
                                 '/HDFEOS/SWATHS/HIRDLS/Data Fields/O3', \
                                 None, None, np.asarray((2,3)))
            self.assertEqual(a.shape[0], 2777)
            self.assertEqual(a.shape[1], 49)

            
if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    #setup test files
    unittest.main()
