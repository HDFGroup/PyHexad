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

class H5writeArray_w_createTest(unittest.TestCase):


    def test_create_array_int(self):
        file_name = get_temp_file()

        with h5py.File(file_name) as loc:

            shape = (32,)
            a = np.zeros(shape, dtype=int)
            path = '/int/32'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)
            
            shape = (32,1)
            a = np.zeros(shape, dtype=np.uint8)
            path = '/int/32 x 1'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)

            shape = (1, 32)
            a = np.zeros(shape, dtype=np.int64)
            path = '/int/1 x 32'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)

            shape = (8, 16)
            a = np.zeros(shape, dtype=np.uint16)
            path = '/int/8 x 16'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)

            shape = (8, 16, 4)
            a = np.zeros(shape, dtype=int)
            path = '/int/8 x 16 x 4'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)

    def test_create_array_float(self):
        file_name = get_temp_file()

        with h5py.File(file_name) as loc:

            shape = (32,)
            a = np.zeros(shape, dtype=np.float64)
            path = '/float/32'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)
            
            shape = (32,1)
            a = np.zeros(shape, dtype=np.float64)
            path = '/float/32 x 1'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)

            shape = (1, 32)
            a = np.zeros(shape, dtype=np.float32)
            path = '/float/1 x 32'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)

            shape = (8, 16)
            a = np.zeros(shape, dtype=np.float32)
            path = '/float/8 x 16'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)

            shape = (8, 16, 4)
            a = np.zeros(shape, dtype=np.float32)
            path = '/float/8 x 16 x 4'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)

    def test_create_array_string(self):
        file_name = get_temp_file()

        with h5py.File(file_name) as loc:

            shape = (32,)
            a = np.zeros(shape, dtype=np.dtype('|S3'))
            path = '/string/32'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)
            
            shape = (32,1)
            a = np.zeros(shape, dtype=np.dtype('|U2'))
            path = '/string/32 x 1'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)

            shape = (1, 32)
            a = np.zeros(shape, dtype=h5py.special_dtype(vlen=str))
            path = '/string/1 x 32'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)

            shape = (8, 16)
            a = np.zeros(shape, dtype=np.dtype('|S7'))
            path = '/float/8 x 16'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)

            shape = (8, 16, 4)
            a = np.zeros(shape, dtype=np.dtype('|U8'))
            path = '/float/8 x 16 x 4'
            msg = create_array(loc, path, a)
            self.assertEqual(msg, path)

            
if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    #setup test files
    unittest.main()
