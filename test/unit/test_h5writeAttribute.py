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
from pyhexad.h5newGroup import new_group
from pyhexad.h5writeAttribute import set_attribute
from .config import TEST_FILES_DIRECTORY

logger = logging.getLogger(__name__)

def get_test_file(name):
    """ Return the absolute path to the given test file. """
    return os.path.join(TEST_FILES_DIRECTORY, name)

def get_temp_file():
    """ Return the absolute path to a temp file. """
    return tempfile.mktemp('.h5')

class H5writeAttributeTest(unittest.TestCase):

    def test_new_attribute(self):
        file_name = get_temp_file()

        with h5py.File(file_name) as loc:
            
            path = '/A/B/C'
            msg = new_group(loc, path)
            self.assertEqual(msg, path)

            path = '/'
            attname = 'foo'
            attvalue = 'bar'
            msg = set_attribute(loc, path, attname, attvalue)
            self.assertEqual(msg, attname)

            path = '/'
            attname = ' '
            attvalue = ''
            msg = set_attribute(loc, path, attname, attvalue)
            self.assertEqual(msg, attname)

            path = '/A/B'
            attname = 'foo'
            attvalue = 1.23
            msg = set_attribute(loc, path, attname, attvalue)
            self.assertEqual(msg, attname)

            path = '/A/B'
            attname = 'bar'
            attvalue = 123
            msg = set_attribute(loc, path, attname, attvalue)
            self.assertEqual(msg, attname)

            path = '/A/B'
            attname = 'bar'
            attvalue = 3.14
            msg = set_attribute(loc, path, attname, attvalue)
            self.assertEqual(msg, attname)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    #setup test files
    unittest.main()
