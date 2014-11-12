# Standard library imports
import logging
import os
from os.path import isfile
import tempfile
import unittest

# Third-party imports
import numpy as np
import h5py

# Local imports
from pyhexad.h5newArray import new_array
from pyhexad.h5writeArray import create_array, write_array
from .config import TEST_FILES_DIRECTORY

logger = logging.getLogger(__name__)

def get_test_file(name):
    """ Return the absolute path to the given test file. """
    return os.path.join(TEST_FILES_DIRECTORY, name)

def get_temp_file():
    """ Return the absolute path to a temp file. """
    return tempfile.mktemp('.h5')

class H5writeArrayTest(unittest.TestCase):

    def test_create_array(self):
        file_name = get_temp_file()

        with h5py.File(file_name) as loc:

            # float64
            shape = (64)
            a = np.zeros(shape)
            path = '/A/B/C/1D'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)

            shape = (1, 32)
            a = np.zeros(shape)
            path = '/A/B/C/1C'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)
            
            shape = (32, 16)
            a = np.zeros(shape)
            path = '/A/B/C/2D'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)

            # this will not happen in Excel, but...
            shape = (2, 3, 4)
            a = np.zeros(shape)
            path = '/A/B/C/3D'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)

            # strings
            shape = (128, 1)
            a = np.zeros(shape, dtype=h5py.special_dtype(vlen=unicode))
            a[...] = u"Hello, World!"
            path = '/A/B/C/1R'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)

            # uint8
            shape = (128, 1)
            a = np.zeros(shape, dtype=np.uint8)
            a[:] = 254
            path = '/A/B/C/1U'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)


    def test_write_array1D(self):
        file_name = get_temp_file()

        with h5py.File(file_name) as loc:

            a = np.zeros(128)
            path = '/1D'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)
            a[:] = 123.45
            msg = write_array(loc, path, a, (slice(0, 128, 1),))
            self.assertEqual(msg, path)

            shape = (1, 128)
            a = np.zeros(shape)
            path = '/1C'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)
            b = np.zeros(64)
            b[:] = 1.0
            # [0:64] -> [0:1:1,0:64:1]
            msg = write_array(loc, path, b, (slice(0, 1, 1), slice(0,64,1)))
            self.assertEqual(msg, path)


    def test_write_array2D(self):
        file_name = get_temp_file()

        with h5py.File(file_name) as loc:

            shape = (1, 128, 64)
            a = np.zeros(shape)
            path = '/1CC'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)
            b = np.zeros(64)
            b[:] = 1.0
            # [0:64] -> [0:1:1, 2:3:1, 0:64:1]
            msg = write_array(loc, path, b, (slice(0, 1, 1), slice(2,3,1), \
                                             slice(0, 64, 1)))
            self.assertEqual(msg, path)

            shape = (16, 32)
            a = np.zeros(shape)
            path = '/2D'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)
            b = np.zeros(64)
            b[:] = 1.0
            # [0:64] -> [0:8:1, 0:8:1]
            msg = write_array(loc, path, b, (slice(0, 8, 1), slice(0,8,1)))
            self.assertEqual(msg, path)


    def test_write_array1D_w_extend(self):
        file_name = get_temp_file()

        with h5py.File(file_name) as loc:

            path = '/1D'
            size = [[-12]]
            plist = 'Datatype,single,Chunksize,[3]'
            msg = new_array(loc, path, size, plist)
            self.assertEqual(msg, path)
            a = np.zeros(128)
            a[:] = 123.45
            msg = write_array(loc, path, a, (slice(0, 128, 1),))
            self.assertEqual(msg, path)

            path = '/1C'
            size = [[-1,-24]]
            plist = 'Datatype,single,Chunksize,[2 3]'
            msg = new_array(loc, path, size, plist)
            self.assertEqual(msg, path)
            b = np.zeros(64)
            b[:] = 1.0
            # [0:64] -> [0:1:1,0:64:1]
            msg = write_array(loc, path, b, (slice(0, 1, 1), slice(0,64,1)))
            self.assertEqual(msg, path)

    def test_write_array2D_w_extend(self):
        file_name = get_temp_file()

        with h5py.File(file_name) as loc:

            path = '/1CC'
            size = [[-1, 12, -32]]
            plist = 'Datatype,single'
            msg = new_array(loc, path, size, plist)
            self.assertEqual(msg, path)            
            b = np.zeros(64)
            b[:] = 1.0
            # [0:64] -> [0:1:1, 2:3:1, 0:64:1]
            msg = write_array(loc, path, b, (slice(0, 1, 1), slice(2,3,1), \
                                             slice(0, 64, 1)))
            self.assertEqual(msg, path)

            path = '/2D'
            size = [[-3, -3]]
            plist = 'Datatype,single,Deflate,6'
            msg = new_array(loc, path, size, plist)
            self.assertEqual(msg, path)            
            b = np.zeros(64)
            b[:] = 1.0
            # [0:64] -> [0:8:1, 0:8:1]
            msg = write_array(loc, path, b, (slice(0, 8, 1), slice(0,8,1)))
            self.assertEqual(msg, path)

            
if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    #setup test files
    unittest.main()
