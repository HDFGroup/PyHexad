
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
def h5disp2(filename,location=None):
    """
    Display detailed information about a specific location in an HDF5 file.
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

        if not location in f:
            return "Invalid location specified."

        obj = f[location]
        cls = f.get(location,getclass=True)
        
        # reset the currents
        global current_row, current_col
        current_row = 0
        current_col = 0

        # generate the display

        # TODO: for now we hardcode a 120x40 display. Fix this!
        MAX_ROW = 120
        MAX_COL = 40
        dty = h5py.special_dtype(vlen=str)
        a = np.empty((MAX_ROW, MAX_COL), dtype=dty)

        path = obj.name

        # render attributes
        
        if cls == h5py.Group or cls == h5py.Dataset or cls == h5py.NamedDatatype:
            
            num_attr = len(obj.attrs)
            row = current_row
            col = current_col
            if num_attr > 0:
                a[row,col] = 'Number of attributes:'
                a[row,col+1] = num_attr
                row += 1
                
                keys = obj.attrs.keys()
                vals = obj.attrs.values()
                for i in range(min(MAX_ROW, num_attr)):
                    a[row+i,col+1] = keys[i]
                    a[row+i,col+2] = str(vals[i])
                row += num_attr
                
                current_row = row + 2

        # render object specific stuff
                
        row = current_row
        col = current_col

        if cls == h5py.Group:

            num_links = len(obj.keys())
            a[row,col] = 'Number of links:'
            a[row,col+1] = num_links
            if num_links > 0:
                a[row+1,col] = 'Link names:'
                for i in range(min(MAX_ROW,num_links)):
                    a[row+1+i,col+1] = obj.keys()[i]
            current_row += num_links+2
                    
        elif cls == h5py.Dataset:

            a[row,col] = 'Number of elements:'
            a[row,col+1] = obj.size
            row += 1

            a[row,col] = 'Shape:'
            if len(obj.shape) > 0:
                for i in range(len(obj.shape)):
                    a[row,col+1+i] = obj.shape[i]
            else:
                a[row,col+1] = '()'
            row += 1
                
            a[row,col] = 'Type:'
            a[row,col+1] = str(obj.dtype)
            row += 1
            
            current_row = row + 2

        else:
            a[current_row, current_col] = path
        
        #if current_row < MAX_ROW and current_col < MAX_COL:

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
