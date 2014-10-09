
import automation
import functools
from functools import partial
import h5py
import h5xl
import logging
import numpy as np
import posixpath
import pyxll
from pyxll import xl_arg_doc, xl_func

_log = logging.getLogger(__name__)

current_idx = 1
max_col = 0

#===============================================================================

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_func("string filename : string",
         category="HDF5",
         thread_safe=False,
         macro=True,
         disable_function_wizard_calc=True)
def h5disp(filename, location=None):
    """
    Display contents of an HDF5 file
    """

#===============================================================================

    if not isinstance(filename, str):
        raise TypeError, 'String expected.'

    if location is not None:
        if not isinstance(location, str):
            raise TypeError, 'String expected.'

    ret = None
    
    if not h5xl.file_exists(filename):
        return "Can't open file."

    with h5py.File(filename, 'r') as f:

        # reset the currents
        global current_idx, max_col
        current_idx = 1
        max_col = 0
        
        lines = []

        # render the root group
        lines.append((0, 1, '/'))

        def print_obj(grp, name):

            global current_idx, max_col

            path = posixpath.join(grp.name, name)

            current_col = path.count('/')
            if max_col < current_col: max_col = current_col

            if grp.get(name, getclass=True) == h5py.Group:
                lines.append((current_idx, current_col, path))
            else:
                lines.append((current_idx, current_col, path.split('/')[-1]))

            current_idx += 1

        f.visit(partial(print_obj, f))

        # generate the display

        dty = h5py.special_dtype(vlen=str)
        a = np.empty((len(lines)+1, max_col+1), dtype=dty)

        current_row = 0

        for i in range(len(lines)):
            a[current_row,0] = lines[i][0]
            a[current_row,lines[i][1]] = lines[i][2]
            current_row += 1
        
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
