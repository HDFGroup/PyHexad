# We use H5Ovisit to traverse the hierarchy starting from a given location.
# We render the structure in tabular form where objects in an HDF5 group
# are listed under that group heading. The table is sparse, because most
# attributes apply only to certain object types.

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
import type_helpers
from type_helpers import is_supported_h5array_type, is_supported_h5table_type

_log = logging.getLogger(__name__)

#===============================================================================

# the table heading layout, more columns to follow...

col_offset = (
    # (key, offset, display name)
    ('INDEX',    0, 'INDEX'),
    ('OBJ_TYPE', 1, 'OBJECT TYPE'),
    ('NAME',     2, 'OBJECT NAME'),
    ('#ATTR',    3, '#ATTRIBUTES'),
    ('#LNK',     4, '#LINKS'),
    ('DTYPE',    5, 'DATA TYPE'),
    ('RANK',     6, 'RANK'),
    ('DSPACE',   7, 'DATA SPACE')
)

#===============================================================================

def render(grp, name):
    """
    render function for HDF5 objects
    """

    if not (isinstance(grp, h5py.File) or isinstance(grp, h5py.Group)):
        raise TypeError, 'HDF5 file or group expected.'

    if not isinstance(name, basestring):
        raise TypeError, 'String expected.'
    
    path = posixpath.join(grp.name, name)    
    obj = grp[name]
    obj_type = grp.get(name, getclass=True)

    if obj_type == h5py.Group:

        return {
            'OBJ_TYPE': 'GROUP',
            'NAME': path,
            '#ATTR': len(obj.attrs.keys()),
            '#LNK': len(obj.keys())
        }

    elif obj_type == h5py.Dataset:

        # determine what kind of dataset
        flavor = 'DATASET'
        dty = obj.dtype
        if is_supported_h5array_type(dty):
            flavor = 'ARRAY'
        elif is_supported_h5table_type(dty):
            flavor = 'TABLE'

        return {
            'OBJ_TYPE': flavor,
            'NAME': name.split('/')[-1],
            '#ATTR': len(obj.attrs.keys()),
            'DTYPE': str(obj.dtype),
            'RANK': len(obj.shape),
            'DSPACE': str(obj.shape)
        }

    elif obj_type == h5py.Datatype:

        return {
            'OBJ_TYPE': obj_type,
            'NAME': name.split('/')[-1],
            '#ATTR': len(obj.attrs.keys()),
            'DTYPE': str(obj.dtype),
        }

    else:
        return {
            'OBJ_TYPE': str(obj_type),
            'NAME': name.split('/')[-1],
        }

#===============================================================================

def render_table(loc):

    result = []

    # line for table heading
    ht = {}
    for c in col_offset:
        ht[c[0]] = c[2]
    result.append(ht)

    if isinstance(loc, h5py.File) or isinstance(loc, h5py.Group):

        # patch the name for the root group
        name = loc.name.split('/')[-1]
        if name == '': name = '/'
        
        result.append(render(loc.parent, name))

        #======================================================================
        # this is the callback for rendering links
        def print_obj(grp, name):
            result.append(render(grp, name))
        #
        #======================================================================

        loc.visit(partial(print_obj, loc))
        
    elif isinstance(loc, h5py.Dataset) or isintance(loc, h5py.Datatype) or \
         isinstance(loc, h5py.SoftLink) or isinstance(loc, h5py.ExternalLink):

        result.append(render(loc.parent, loc.name.split('/')[-1]))

    else:
        raise TypeError, "'location' is not an HDF5 handle."

    return result

#===============================================================================

@xl_func("string filename, string location : string",
         category="HDF5",
         thread_safe=False,
         macro=True,
         disable_function_wizard_calc=True)
def h5showList(filename, location):
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

    with h5py.File(filename, 'r') as f:

        hnd = f
        if location != '':
            if not location in f:
                return 'Invalid location.'
            else:
                hnd = f[location]

        # render the tree as a list of lines

        lines = render_table(hnd)
        
        if len(lines) >= Limits.EXCEL_MAX_ROWS:
            return 'The number objects in the file exceeds the maximum number' \
                'of rows of an Excel worksheet.'
            
        # generate the display in a Numpy array & patch in the INDEX column

        dty = h5py.special_dtype(vlen=str)
        a = np.empty((len(lines), len(col_offset)), dtype=dty)

        row = 0
        
        for i in range(0,len(lines)):
            a[row, 0] = row-1
            for k in col_offset:
                key = k[0]
                col = k[1]
                if key in lines[i].keys():
                    a[row, col] = lines[i][key]
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
                                     range.Resize(a.shape[0]+1, a.shape[1]))
                    range.Value = np.asarray(a, dtype=dty)

            except Exception, ex:
                _log.info(ex)
                ret = 'Internal error.'
        #
        #=======================================================================

        # kick off the asynchronous call to the update function
        pyxll.async_call(update_func)

        return '\0'
