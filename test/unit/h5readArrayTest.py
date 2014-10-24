
import sys
sys.path.append('../..')
sys.path.append('../../pyhexad')

import pyhexad
from pyhexad.h5readArray import get_ndarray

import config
import h5py
import logging
import numpy as np
import os
import os.path as op
import shutil
import stat

import unittest

def getFile(name, tgt=None, ro=False):
    src = config.get('testfiledir') + name
    logging.info("copying file to this directory: " + src)
    if not tgt:
        tgt = name
    if op.isfile(tgt):
        # make sure it's writable, before we copy over it
        os.chmod(tgt, stat.S_IWRITE|stat.S_IREAD)
    shutil.copyfile(src, tgt)
    if ro:
        logging.info('make read-only')
        os.chmod(tgt, stat.S_IREAD)

class h5readArrayTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(h5readArrayTest, self).__init__(*args, **kwargs)
        # main
        logging.info('init!')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def test6(self):
        file_name = 'hdfeos5.h5'
        getFile(file_name)
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
                                 np.asarray((10,)), np.asarray((20,)),
                                 np.asarray((3,)))
            self.assertEqual(a.size, 4)
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

if __name__ == '__main__':
    #setup test files
    
    unittest.main()
