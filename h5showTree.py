# We use H5Ovisit to traverse the hierarchy starting from a given location.
# H5Ovisit introduces a traversal order that is akin to XML document order.
# A worksheet can be viewed as a 2D grid of rows and columns.
# The cell position where to render the link name of an object is as follows:
#
# row    - the current position in "document order"
# column - the "level" = the number of group ancestors

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

def render_tree(loc):

    result = []
    
    if isinstance(loc, h5py.File) or isinstance(loc, h5py.Group):

        result.append((1, loc.name))

        #======================================================================
        # this is the callback for rendering links
        
        def print_obj(grp, name):

            path = posixpath.join(grp.name, name)
            col = path.count('/')

            # render the full path only for groups
            # otherwise just the link name
            
            if grp.get(name, getclass=True) == h5py.Group:
                result.append((col, path))
            else:
                result.append((col, path.split('/')[-1]))

        #=======================================================================

        loc.visit(partial(print_obj, loc))
        
    elif isinstance(loc, h5py.Dataset) or isintance(loc, h5py.Datatype) or isinstance(loc, h5py.SoftLink) or isinstance(loc, h5py.ExternalLink):
        
        result.append(loc.name)
        
    else:
        raise TypeError, "'location' is not an HDF5 handle."

    # determine the maximum column index
    max_col = 1
    for line in result:
        if line[0] > max_col:
            max_col = line[0]

    return result, max_col

#===============================================================================

@xl_func("string filename, string location : string",
         category="HDF5",
         thread_safe=False,
         macro=True,
         disable_function_wizard_calc=True)
def h5showTree(filename, location):
    """
    Display contents of an HDF5 file in hierarchical form
    filename: the name of an HDF5 file
    location: an HDF5 path name (optional)
    """
    
    if not isinstance(filename, str):
        raise TypeError, "'filename' must be a string."

    if not isinstance(location, str):
            raise TypeError, "'location' must be a string."
            
    if not file_exists(filename):
        return "Can't open file '%s' or the file is not an HDF5 file." % (filename)

    # if a location was specified, we'll find out if it's meaningful only
    # after opening the file

    with h5py.File(filename, 'r') as f:
        
        hnd = f

        if location != '':
            if not location in f:
                return 'Invalid location.'
            else:
                hnd = f[location]

        # render the tree as a list of lines

        lines = []
        max_col = 0
        
        lines, max_col = render_tree(hnd)
        
        if len(lines) >= Limits.EXCEL_MAX_ROWS or max_col >= Limits.EXCEL_MAX_COLS:
            return 'The number objects in the file or the depth of the hierarchy exceeds the maximum number of rows or columns of an Excel worksheet.'
            
        # generate the display in a Numpy array

        dty = h5py.special_dtype(vlen=str)
        a = np.empty((len(lines)+1, max_col+1), dtype=dty)

        row = 0
        for l in lines:
            a[row,0] = row
            a[row, l[0]] = l[1]
            row += 1
        
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
