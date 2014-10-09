
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

col_offset = (
    # (key, offset, display name)
    ('INDEX', 0, 'INDEX'),
    ('OBJ_TYPE', 1, 'OBJECT TYPE'),
    ('NAME', 2, 'OBJECT NAME'),
    ('#ATTR', 3, '#ATTRIBUTES'),
    ('#LNK', 4, '#LINKS'),
    ('DTYPE', 5, 'DATA TYPE'),
    ('RANK', 6, 'RANK'),
    ('DSPACE', 7, 'DATA SPACE')
)

current_idx = 1

#===============================================================================

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_func("string filename : string",
         category="HDF5",
         thread_safe=False,
         macro=True,
         disable_function_wizard_calc=True)
def h5list(filename):
    """
    Display contents of an HDF5 file in tabular form
    """

#===============================================================================

    ret = None
    
    if not h5xl.file_exists(filename):
        return "Can't open file."

    with h5py.File(filename, 'r') as f:

        # reset the currents
        global current_idx, current_row
        current_idx = 1
        current_row = 0

        lines = []
        
        # the header line
        ht = {}
        for c in col_offset:
            ht[c[0]] = c[2]
        lines.append(ht)

        # render the root group
        lines.append(
            {
                'INDEX': 0,
                'OBJ_TYPE': 'GROUP',
                'NAME': '/',
                '#ATTR': len(f.attrs.keys()),
                '#LNK': len(f.keys())
            })
        
        def print_obj(grp, name):

            global current_idx
            
            path = posixpath.join(grp.name, name)
            
            obj = grp[name]
            obj_type = grp.get(name, getclass=True)
                
            if obj_type == h5py.Group:
                lines.append(
                    {
                        'INDEX': current_idx,
                        'OBJ_TYPE': 'GROUP',
                        'NAME': path,
                        '#ATTR': len(obj.attrs.keys()),
                        '#LNK': len(obj.keys())
                    })

            elif obj_type == h5py.Dataset:
                lines.append(
                    {
                        'INDEX': current_idx,
                        'OBJ_TYPE': 'DATASET',
                        'NAME': name.split('/')[-1],
                        '#ATTR': len(obj.attrs.keys()),
                        'DTYPE': str(obj.dtype),
                        'RANK': len(obj.shape),
                        'DSPACE': str(obj.shape)
                    })

            else:
                lines.append(
                    {
                        'INDEX': current_idx,
                        'OBJ_TYPE': str(obj_type),
                        'NAME': name.split('/')[-1],
                    })
                
            current_idx += 1

        f.visit(partial(print_obj, f))

        # generate the display

        dty = h5py.special_dtype(vlen=str)
        a = np.empty((2*len(lines), len(col_offset)), dtype=dty)

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
