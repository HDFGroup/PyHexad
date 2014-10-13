"""
Display detailed information about HDF5 objects, including HDF5 attributes
and their values.
"""

import automation
import config
from config import Limits
import file_helpers
from file_helpers import file_exists
import functools
from functools import partial
import h5py
import logging
import numpy as np
import posixpath
import pyxll
from pyxll import xl_arg_doc, xl_func

_log = logging.getLogger(__name__)

#===============================================================================

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_arg_doc("location", "An HDF5 path name.")
@xl_func("string filename, string location : var",
         category="HDF5",
         thread_safe=False,
         macro=True,
         disable_function_wizard_calc=True)
def h5disp(filename,location):
    """
    Display detailed information about a specific location in an HDF5 file.
    """

#===============================================================================

    if not isinstance(filename, str):
        return "'filename' must be a string."

    if not isinstance(location, str):
        return "'location' must be a string."
            
    if not file_exists(filename):
        return "Can't open file."

    with h5py.File(filename, 'r') as f:

        if not location in f:
            return 'Invalid location.'

        obj = f[location]
        cls = f.get(location,getclass=True)
        
        # generate the display - at the moment there are only two columns

        lines = []

        path = obj.name

        # render attributes
        
        if cls == h5py.Group or cls == h5py.Dataset or cls == h5py.NamedDatatype:
            
            num_attr = len(obj.attrs)
            if num_attr > 0:
                lines.append(('Number of attributes:', num_attr))
                keys = obj.attrs.keys()
                vals = obj.attrs.values()
                for i in range(num_attr):
                    lines.append((keys[i], str(vals[i])))
        
        # render object specific stuff
                
        if cls == h5py.Group:
            
            num_links = len(obj.keys())
            lines.append(('Number of links:', num_links))
            if num_links > 0:
                lines.append(('Link names:', '\0'))
                for i in range(num_links):
                    lines.append(('\0', obj.keys()[i]))

        elif cls == h5py.Dataset:

            lines.append(('Number of elements:', obj.size))
            lines.append(('Shape:', str(obj.shape)))
            lines.append(('Type:', str(obj.dtype)))

        else:
            pass


        # copy lines into Numpy array
        # Is that really necessary?
            
        dty = h5py.special_dtype(vlen=str)
        a = np.empty((len(lines)+1, 2), dtype=dty)

        row = 0
        for l in lines:
            a[row] = l
            row += 1
            if row >= Limits.EXCEL_MAX_ROWS:
                break
        
        # get the address of the calling cell using xlfCaller
        caller = pyxll.xlfCaller()
        address = caller.address

        #=======================================================================
        # the update is done asynchronously so as not to block some
        # versions of Excel by updating the worksheet from a worksheet function
        def update_func():
            xl = automation.xl_app()
            range = xl.Range(address)
            
            try:
                with h5py.File(filename, 'r') as f:
                    range = xl.Range(range.Resize(2,1),
                                     range.Resize(a.shape[0], a.shape[1]))
                    range.Value = np.asarray(a, dtype=dty)

            except Exception, ex:
                _log.info(ex)
                ret = 'Internal error.'
        #=======================================================================

        # kick off the asynchronous call to the update function
        pyxll.async_call(update_func)

        return '\0'
