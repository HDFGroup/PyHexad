
import h5py
import h5xl
import logging
import numpy as np
import pyxll
from pyxll import xl_arg_doc, xl_func

_log = logging.getLogger(__name__)

#===============================================================================

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_arg_doc("location", "The location of the object (attribute owner).")
@xl_arg_doc("attname", "The attribute name.")
@xl_arg_doc("attvalue", "The attribute value.")
@xl_func("string filename, string location, string attname, var attvalue: var",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=True)
def h5writeattr(filename, location, attname, attvalue):
    """
    Writes the value of an HDF5 attribute

    Existing attributes will be overwritten.
    """

#===============================================================================

    if not isinstance(filename, str):
        raise TypeError, 'String expected.'
        
    if not isinstance(location, str):
        raise TypeError, 'String expected.'
        
    if not isinstance(attname, str):
        raise TypeError, 'String expected.'

    if attval is None:
        raise ValueError, 'Value expected.'
        
    ret = None

    if not h5xl.file_exists(filename):
        return "Can't open file."

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

                ret = attvalue
            else:
                return "Invalid location '%s'." % (location)
                    
    except Exception, ex:
        _log.info(ex)
        return 'Internal error.'

    return ret
