
import pyxll
from pyxll import xl_arg_doc, xl_func
import h5py
import h5xl

import logging
_log = logging.getLogger(__name__)

#===============================================================================

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_arg_doc("location", "The location of the object (attribute owner).")
@xl_arg_doc("attr", "The attribute's name.")
@xl_func("string filename, string location, string attr: var",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=True)
def h5readattr(filename, location, attr):
    """
    Reads and returns the value of an HDF5 attribute.
    """

#===============================================================================

    if not h5xl.file_exists(filename):
        return "Can't open file."

    with h5py.File(filename, 'r') as f:
        try:
            if location in f: # valid location?
                cls = f.get(location, getclass=True)
                if (cls == h5py.Dataset or cls == h5py.Group): # object?
                    if attr in f[location].attrs: # valid attribute name?
                        # best effort to read the attribute
                        # string instead of typed value... (TODO: Fix this!)
                        return str(f[location].attrs[attr])
                    else:
                        return "Can't open attribute."
                else:
                    return "No object at location."
            else:
                return "Can't open location."
        except Exception, e:
            _log.info(e)
            return "Internal error."
