
import automation
from automation import xl_app
import pyxll
from pyxll import xl_arg_doc, xl_func
import h5py
import h5xl

import logging
_log = logging.getLogger(__name__)

import os

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_arg_doc("location", "The location of the HDF5 image (dataset).")
@xl_func("string filename, string location: string", category="HDF5")
def h5readimg(filename, location):
    """Reads an HDF5 image (dataset)"""
    
    if not isinstance(filename, str):
        raise TypeError, 'String expected.'

    if not isinstance(location, str):
        raise TypeError, 'String expected.'

    try:
        with h5py.File(filename) as f:
            # find the dataset and render the image in a temporary file
            # fake it for now...
            img = os.path.dirname(xl_app().ActiveWorkbook.FullName)
            img += "\\h5py.jpg"
            xl_app().ActiveSheet.Pictures().Insert(img)
                    
    except IOError, io:
        h5xl.popup("Error", "Can't open or create file\n'%s'." % (filename))

    return location
