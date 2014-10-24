
import automation
import file_helpers
from file_helpers import file_exists
import h5_helpers
from h5_helpers import path_is_valid_wrt_loc
import h5py
import logging
import numpy as np
import pyxll
from pyxll import xl_func
import shape_helpers
from shape_helpers import is_valid_hyperslab_spec
import type_helpers
from type_helpers import is_supported_h5array_type, excel_dtype

_log = logging.getLogger(__name__)

#===============================================================================

def get_ndarray(loc, path, first = None, last = None, step = None):

    # Is this a valid location?
    is_valid, species = path_is_valid_wrt_loc(loc, path)
    if not is_valid:
        return (None, 'Invalid location specified.')
        
    # Do we have a dataset?
    if (loc.get(path) is None) or \
       (loc.get(path, getclass=True) != h5py.Dataset):
        return (None, "Can't open HDF5 array '%s'." % (arrayname))
            
    dst = loc[path]

    # Does it have the right shape?
    # TODO: how does h5py represent NULL dataspaces?
    dsp = dst.shape
    if len(dsp) > 2: return (None, 'Unsupported dataset shape.')

    # Does it have the right type?
    dty = dst.dtype
    if not is_supported_h5array_type(dty):
        return None, 'Unsupported dataset element type.'

    # Is the hyperslab selection meaningful?
    if not is_valid_hyperslab_spec(np.asarray(dsp), first, last, step):
        return None, 'Invalid hyperslab specification.'

    # The hyperslab selection is 1-based => Convert it to 0-based Numpy notation.
    rk = len(dsp)
    if rk == 1:
        
        start = 0
        stop = dsp[0]
        stride = 1

        if first is not None:
            start = first[0]-1
        if last is not None:
            stop = last[0]
        if step is not None:
            stride = step[0]

        slc = slice(start, stop, stride)
        x = dst[slc]

        return (x, '%d x 1' % x.size)
        
    elif rk == 2:

        (None, 'Unimplemented.')

    else:
        
        return (None, 'Unsupported HDF5 array rank.')
    
    return (None, 'Error')

#===============================================================================

@xl_func("string filename, string arrayname, numpy_array<int> first, numpy_array<int> last, numpy_array<int> step : string",
         category="HDF5",
         thread_safe=False,
         macro=True,
         disable_function_wizard_calc=True)
def h5readArray(filename, arrayname, first, last, step):
    """
    Reads elements of an HDF5 array. Specify a rectilinear (strided) subregion
    via 'first' and 'last' ('stride').
    
    :param filename: the name of an HDF5 file
    :param arrayname: the name of an HDF5 array
    :param first: the (one-based) index of the first element to be read (optional)
    :param last: the (one-based) index of the last element to be read (optional)
    :param stride: the read stride in each dimension
    :returns: A string
    """

#===============================================================================

    # sanity check

    if not isinstance(filename, str):
        raise TypeError, "'filename' must be a string."
    if not isinstance(arrayname, str):
            raise TypeError, "'arrayname' must be a string."
    if first is not None:
        if not isinstance(first, np.ndarray):
            raise TypeError, "'first' must be a Numpy ndarray."
    if last is not None:
        if not isinstance(last, np.ndarray):
            raise TypeError, "'last' must be a Numpy ndarray."
    if first is not None:
        if not isinstance(step, np.ndarray):
            raise TypeError, "'step' must be a Numpy ndarray."
    if not file_exists(filename):
        return "Can't open file '%s' or the file is not an HDF5 file." %  \
            (filename)

    ret = '\0'
    
    with h5py.File(filename, 'r') as f:

        x, ret = get_ndarray(f, arrayname, first, last, step)

        if x is not None:
            ret = renderer.draw(x)
        
    return ret
