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
import renderer
from renderer import draw

_log = logging.getLogger(__name__)

#===============================================================================

def render_tree(loc):
    # Create a list of tuples (col, name), where 'col' is the
    # column index and 'name' is a link or HDF5 path name.
    # The row index is the position in the list.
    #
    # Returns the list and the maximum column index.
    
    result = []
    
    if isinstance(loc, h5py.File) or isinstance(loc, h5py.Group):

        result.append((1, loc.name))

        #======================================================================
        # this is the callback for rendering links
        #
        def print_obj(grp, name):

            path = posixpath.join(grp.name, name)
            col = path.count('/')

            # render the full path only for groups
            # otherwise just the link name
            
            if grp.get(name, getclass=True) == h5py.Group:
                result.append((col, path))
            else:
                result.append((col, path.split('/')[-1]))
        #
        #=======================================================================

        loc.visit(partial(print_obj, loc))
        
    elif isinstance(loc, h5py.Dataset) or isintance(loc, h5py.Datatype) or \
         isinstance(loc, h5py.SoftLink) or isinstance(loc, h5py.ExternalLink):
        
        result.append((1, loc.name))
        
    else:
        raise TypeError, "'location' is not an HDF5 handle."

    # determine the maximum column index
    max_col = 1
    for line in result:
        if line[0] > max_col: max_col = line[0]

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
    
    :param filename: the name of an HDF5 file
    :param location: an HDF5 path name (optional)
    :returns: A string
    """
    
    if not isinstance(filename, str):
        raise TypeError, "'filename' must be a string."

    if not isinstance(location, str):
            raise TypeError, "'location' must be a string."
            
    if not file_exists(filename):
        return "Can't open file '%s' or the file is not an HDF5 file." %  \
            (filename)

    ret = '\0'
    
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
        
        if len(lines) >= Limits.EXCEL_MAX_ROWS or \
           max_col >= Limits.EXCEL_MAX_COLS:
            return 'The number objects in the file or the depth of the' \
                'hierarchy exceeds the maximum number of rows or columns' \
                'of an Excel worksheet.'
            
        # generate the display in a Numpy array

        dty = h5py.special_dtype(vlen=str)
        a = np.empty((len(lines)+1, max_col+1), dtype=dty)

        # add row numbers on the fly
        
        row = 0
        # l -> (col, name)
        for l in lines:
            a[row,0] = row
            a[row, l[0]] = l[1]
            row += 1
        
        renderer.draw(a)

        return ret
