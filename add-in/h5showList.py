"""
We use H5Ovisit to traverse the hierarchy starting from a given location.
We render the structure in tabular form where objects in an HDF5 group
are listed under that group heading. The table is sparse, because most
attributes apply only to certain object types.
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
import type_helpers
from type_helpers import is_supported_h5array_type, is_supported_h5table_type

_log = logging.getLogger(__name__)

# the heading layout

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

# global index

current_idx = 0

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

    global current_idx
    
    if obj_type == h5py.Group:
        return {
            'INDEX': current_idx,
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
            'INDEX': current_idx,
            'OBJ_TYPE': flavor,
            'NAME': name.split('/')[-1],
            '#ATTR': len(obj.attrs.keys()),
            'DTYPE': str(obj.dtype),
            'RANK': len(obj.shape),
            'DSPACE': str(obj.shape)
        }
    else:
        return {
            'INDEX': current_idx,
            'OBJ_TYPE': str(obj_type),
            'NAME': name.split('/')[-1],
        }

#===============================================================================

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_arg_doc("location", "An HDF5 path name.")
@xl_func("string filename, string location : var",
         category="HDF5",
         thread_safe=False,
         macro=True,
         disable_function_wizard_calc=True)
def h5showList(filename, location):
    """
    Display contents of an HDF5 file in tabular form
    """

#===============================================================================


    if not isinstance(filename, str):
        return "'filename' must be a string."

    if location is not None:
        if not isinstance(location, str):
            return "'location' must be a string."
            
    if not file_exists(filename):
        return "Can't open file."

    with h5py.File(filename, 'r') as f:

        # initialize the current position
        
        global current_idx
        current_idx = 0
        
        # this is our "screen", which consists of lines
                
        lines = []
        
        # determine the base location, type, and render it
        
        base = f
        base_type = h5py.Group

        if location != '':
            if not location in f:
                return 'Invalid location.'
            else:
                base = f[location]
                base_type = f.get(location, getclass=True)                
                baseline = render(f, location)
        else:
            baseline = {
                'INDEX': current_idx,
                'OBJ_TYPE': 'GROUP',
                'NAME': '/',
                '#ATTR': len(f.attrs.keys()),
                '#LNK': len(f.keys())
            }
        current_idx += 1
        
        ht = {}
        for c in col_offset:
            ht[c[0]] = c[2]
        lines.append(ht)
        lines.append(baseline)
        
        #======================================================================
        # this is the callback for rendering links

        def print_obj(grp, name):
            global current_idx            
            lines.append(render(grp, name))
            current_idx += 1
            
        #======================================================================

        # if this is an HDF5  group, start "going places"
            
        if base_type == h5py.Group:
            base.visit(partial(print_obj, base))

        # generate the display

        dty = h5py.special_dtype(vlen=str)
        a = np.empty((2*len(lines), len(col_offset)), dtype=dty)

        current_row = 0
        
        # render the header row

        for k in col_offset:
            a[current_row,k[1]] = lines[0][k[0]]
        current_row += 1

        # render the root group
        for k in col_offset:
            if k[0] in lines[1].keys():
                a[current_row,k[1]] = lines[1][k[0]]
        current_row += 1

        #render the rest
        for i in range(2,len(lines)):
            if lines[i]['OBJ_TYPE'] == 'GROUP':
                current_row += 1
            for k in col_offset:
                if k[0] in lines[i].keys():
                    a[current_row,k[1]] = lines[i][k[0]]
            current_row += 1

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
