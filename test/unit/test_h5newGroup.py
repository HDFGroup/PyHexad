# Standard library imports
import logging
import os
from os.path import isfile
import tempfile
import unittest

# Third-party imports
import h5py

# Local imports
from pyhexad.h5newGroup import new_group
from .config import TEST_FILES_DIRECTORY

logger = logging.getLogger(__name__)

def get_test_file(name):
    """ Return the absolute path to the given test file. """
    return os.path.join(TEST_FILES_DIRECTORY, name)

def get_temp_file():
    """ Return the absolute path to a temp file. """
    return tempfile.mktemp('.h5')

class H5newGroupTest(unittest.TestCase):

    def test_new_group(self):
        file_name = get_temp_file()

        with h5py.File(file_name) as loc:
            
            # vanilla

            path = '/A/B/C/D'
            msg = new_group(loc, path)
            self.assertEqual(msg, path)

            path = '/'
            msg = new_group(loc, path)
            self.assertEqual(msg, path)

            # throw in a soft link

            loc['/A/B/softD'] = h5py.SoftLink('/A/B/C/D')
            path = 'This works!'
            msg = new_group(loc, 'This works!')
            self.assertEqual(msg, path)

            # failures

            loc['/A/B/softlink'] = h5py.SoftLink('/some/path')
            path = '/A/B/softlink/C'
            msg = new_group(loc, '/A/B/softlink/C')
            self.assertEqual(msg, "Can't create group at '%s'." % (path))
            path = 'softlink/C'
            msg = new_group(loc['/A/B'], path)
            self.assertEqual(msg, "Can't create group at '%s'." % (path))


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    #setup test files
    unittest.main()
