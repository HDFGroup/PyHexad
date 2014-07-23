
import automation
import pyxll
from pyxll import xl_arg_doc, xl_func
import h5py
import h5xl
import numpy as np
import posixpath
import functools
from functools import partial

import logging
_log = logging.getLogger(__name__)

current_row = 0
current_col = 0

#===============================================================================

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_arg_doc("location", "An HDF5 path name.")
@xl_func("string filename, string location : string",
         category="HDF5",
         thread_safe=False,
         macro=True,
         disable_function_wizard_calc=True)
def h5disp2(filename,location):
    """
    Display detailed contents of an HDF5 file starting at a specific location.
    """

#===============================================================================

    ret = None
    
    if not h5xl.file_exists(filename):
        return "Can't open file."

    with h5py.File(filename, 'r') as f:

        if not location in f:
            return "Invalid location specified."

        # check if we have a group, use parent if not
        start_grp = f
        obj = f[location]
        if f.get(location,getclass=True) != h5py.Group:
            start_grp = obj.parent
        else:
            start_grp = obj
            
        # reset the currents
        global current_row, current_col
        current_row = 0
        current_col = 0
        # adjustment needed for the starting column 
        col_offset = start_grp.name.count('/') + 1
        
        # generate the display

        # TODO: for now we hardcode a 120x40 display. Fix this!
        MAX_ROW = 120
        MAX_COL = 40
        dty = h5py.special_dtype(vlen=str)
        a = np.empty((MAX_ROW, MAX_COL), dtype=dty)

        def print_obj(grp, name):

            global current_row, current_col

            path = posixpath.join(grp.name, name)
            current_col = path.count('/') - col_offset

            if current_row < MAX_ROW and current_col < MAX_COL:
                a[current_row, current_col] = path
                current_row += 1

        start_grp.visit(partial(print_obj, start_grp))

        # get the address of the calling cell using xlfCaller
        caller = pyxll.xlfCaller()
        address = caller.address

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

        # kick off the asynchronous call to the update function
        pyxll.async_call(update_func)

        ret = 'Enjoy the show!'
        
        return ret
