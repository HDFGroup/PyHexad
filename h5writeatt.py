
import pyxll
from pyxll import xl_arg_doc, xl_func
import h5py
import h5xl

import logging
_log = logging.getLogger(__name__)

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_arg_doc("location", "The location of the object (attribute owner).")
@xl_arg_doc("attname", "The attribute's name.")
@xl_arg_doc("attvalue", "The attribute's value.")
@xl_func("string filename, string location, string attname, var attvalue: var",
         category="HDF5")
def h5writeattr(filename, location, attname, attvalue):
    """Writes or updates the value of an HDF5 attribute"""
            
    try:
        with h5py.File(filename) as f:
            if location in f:
                # see if we've got a number or a string
                if isinstance(attvalue, (int, long, float)):
                    # it's an integer
                    if float(int(attvalue)) == float(attvalue):
                        f[location].attrs.create(attname, int(attvalue),
                                                 dtype='i4')
                    else:
                        f[location].attrs[attname] = attvalue
                else:
                    f[location].attrs[attname] = str(attvalue)
            else:
                h5xl.popup("Error", "Invalid location\n'%s'." % (location))
                    
    except IOError, io:
        h5xl.popup("Error", "Can't open or create file\n'%s'." % (filename))

    return attvalue
