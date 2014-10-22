
import sys
sys.path.append('../..')
sys.path.append('../../pyhexad')

import pyhexad
from pyhexad.h5getInfo import render_info

import config
import h5py
import logging
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

class h5getInfoTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(h5getInfoTest, self).__init__(*args, **kwargs)
        # main
        logging.info('init!')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def test1(self):
        file_name = 'cadchftickdata.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 8)
            lst = render_info(loc, '/18-09-2011')
            self.assertEqual(len(lst), 3)
            self.assertRaises(TypeError, render_info, 'Hello, World!')
            
    def test2(self):
        file_name = 'compound.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 5)

    def test3(self):
        file_name = 'compound_attr.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 3)

    def test4(self):
        file_name = 'empty.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 1)

    def test5(self):
        file_name = 'group100.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 102)

    def test6(self):
        file_name = 'hdfeos5.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 4)

    def test7(self):
        file_name = 'namedtype.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 4)
            lst = render_info(loc, 'dtype_simple')
            self.assertEqual(len(lst), 3)

    def test8(self):
        file_name = 'tall.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 7)
            lst = render_info(loc, '/g1/g1.2/g1.2.1')
            self.assertEqual(len(lst), 3)
            lst = render_info(loc, '/g1/g1.2/g1.2.1/slink')
            self.assertEqual(len(lst), 2)

    def test9(self):
        file_name = 'tall_with_udlink.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 7)
            lst = render_info(loc, '/g1/g1.2/extlink')
            self.assertEqual(len(lst), 2)
            self.assertRaises(Exception, render_info, loc, '/g2/udlink')

    def test10(self):
        file_name = 'tgroup.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 5)

    def test11(self):
        file_name = 'tref.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 4)

    def test12(self):
        file_name = 'tstr.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 7)

    def test13(self):
        file_name = 'zerodim.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_info(loc, '/')
            self.assertEqual(len(lst), 3)
            
if __name__ == '__main__':
    #setup test files
    
    unittest.main()
