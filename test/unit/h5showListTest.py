
import sys
sys.path.append('../..')
sys.path.append('../../pyhexad')

import pyhexad
from pyhexad.h5showList import render_table

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

class h5showListTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(h5showListTest, self).__init__(*args, **kwargs)
        # main
        logging.info('init!')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def test1(self):
        file_name = 'cadchftickdata.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_table(loc)
            self.assertEqual(len(lst), 8)

    def test2(self):
        file_name = 'compound.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_table(loc)
            self.assertEqual(len(lst), 3)

    def test3(self):
        file_name = 'compound_attr.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_table(loc)
            self.assertEqual(len(lst), 2)

    def test4(self):
        file_name = 'empty.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_table(loc)
            self.assertEqual(len(lst), 2)

    def test5(self):
        file_name = 'group100.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_table(loc)
            self.assertEqual(len(lst), 102)

    def test6(self):
        file_name = 'hdfeos5.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_table(loc)
            self.assertEqual(len(lst), 102)

    def test7(self):
        file_name = 'namedtype.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_table(loc)
            self.assertEqual(len(lst), 4)

    def test8(self):
        file_name = 'tall.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_table(loc)
            self.assertEqual(len(lst), 11)

    def test8(self):
        file_name = 'tall_with_udlink.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_table(loc)
            self.assertEqual(len(lst), 11)

    def test9(self):
        file_name = 'tgroup.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_table(loc)
            self.assertEqual(len(lst), 15)

    def test9(self):
        file_name = 'tref.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_table(loc)
            self.assertEqual(len(lst), 6)

    def test10(self):
        file_name = 'tstr.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_table(loc)
            self.assertEqual(len(lst), 7)

    def test11(self):
        file_name = 'zerodim.h5'
        getFile(file_name)
        with h5py.File(file_name) as loc:
            lst = render_table(loc)
            self.assertEqual(len(lst), 3)

if __name__ == '__main__':
    #setup test files
    
    unittest.main()
