
import pyxll
from pyxll import xl_arg_doc, xl_func
import h5py
import h5xl

import logging
_log = logging.getLogger(__name__)

#===============================================================================

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_arg_doc("location", "The location of the group.")
@xl_func("string filename, string location: string", category="HDF5")
def h5mkgrp(filename, location):
    """Creates an HDF5 group (and missing intermediate groups and file)"""

#===============================================================================

    if filename.strip() == '':
        return 'Need a file name.'
    if location.strip() == '':
        location = '/'

    try:
        with h5py.File(filename, 'a') as f:
            f.require_group(location)
            return location
                    
    except Exception, e:
        _log.info(e)
        return "Can't open/create file."
