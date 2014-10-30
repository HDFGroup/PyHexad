
import logging
import os
from os.path import isfile
import shutil
import stat
import unittest

import h5py

from pyhexad.h5readImage import get_image
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

class H5readImageTest(unittest.TestCase):

    def test1(self):
        
        file_name = get_test_file('ex_image2.h5')

        with h5py.File(file_name) as loc:
            a, msg = get_image(loc, '/image8bit')
            self.assertTrue(os.path.exists(a))

    def test2(self):
        
        file_name = get_test_file('ex_image3.h5')

        with h5py.File(file_name) as loc:
            a, msg = get_image(loc, '/All data')
            self.assertTrue(os.path.exists(a))

            a, msg = get_image(loc, '/Land data')
            self.assertTrue(os.path.exists(a))

            a, msg = get_image(loc, '/Sea data')
            self.assertTrue(os.path.exists(a))

            a, msg = get_image(loc, '/Sea data', '/Rainbow pallete')
            print msg
            self.assertTrue(os.path.exists(a))


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    #setup test files
    unittest.main()
