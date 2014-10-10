
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

# keep track of the current pixel position in these globals
# TODO: Add safeguards so that we don't exceed the Excel row and column
#       count limits!

current_idx = 1
max_col = 0

#===============================================================================

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_arg_doc("location", "An HDF5 path. (Default: '/')")
@xl_func("string filename, string location : var",
         category="HDF5",
         thread_safe=False,
         macro=True,
         disable_function_wizard_calc=True)
def h5disp(filename, location=None):
    """
    Display contents of an HDF5 file in hierarchical form
    """

#===============================================================================

    """
    We use H5Ovisit to traverse the hierarchy starting from a given location.
    H5Ovisit introduces a traversal order that is akin to XML document order.
    A worksheet can be viewed as a 2D grid of rows and columns.
    The cell position where to render the link name of an object is as follows:

    row    - the current position in "document order"
    column - the "level" = the number of group ancestors
    """

    if not isinstance(filename, str):
        raise TypeError, 'String expected.'

    if location is not None:
        if not isinstance(location, str):
            raise TypeError, 'String expected.'
            
    if not file_exists(filename):
        raise IOError, "Can't open file."

    # if a location was specified, we'll find out if it's meaningful only
    # after opening the file

    with h5py.File(filename, 'r') as f:

        base = f
        if location != '':
            if not location in f:
                return 'Invalid location.'
            else:
                base = f[location]

        # reset the current position
        
        global current_idx, max_col
        current_idx = 1
        max_col = 0

        # this is our "screen", which consists of lines
        
        lines = []

        # render the base location
        
        if base == f:
            lines.append((0, 1, '/'))
        else:
            lines.append((0, 1, base.name))

        # this is the callback for rendering links
        
        def print_obj(grp, name):
            
            global current_idx, max_col

            # make sure we don't "overdraw"
            
            if current_idx >= Limits.EXCEL_MAX_ROWS or max_col >= Limits.EXCEL_MAX_COLS:
                return 1

            path = posixpath.join(grp.name, name)
            
            current_col = path.count('/')
            if max_col < current_col: max_col = current_col

            # render the full path only for groups
            # otherwise just the link name
            
            if grp.get(name, getclass=True) == h5py.Group:
                lines.append((current_idx, current_col, path))
            else:
                lines.append((current_idx, current_col, path.split('/')[-1]))

            current_idx += 1

        # start "going places"
            
        base.visit(partial(print_obj, base))

        # generate the display in a Numpy array
        # QUESTION: is that redundant??? we have a list of lists already...

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

        return '\0'
