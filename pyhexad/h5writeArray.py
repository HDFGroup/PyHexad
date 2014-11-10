
import logging

import h5py
import h5xl
import numpy as np
import pyxll
from pyxll import xl_func

from h5_helpers import is_h5_location_handle, path_is_available_for_obj, \
    resolvable
from shape_helpers import try_intarray
from type_helpers import is_supported_h5array_type

logger = logging.getLogger(__name__)

#==============================================================================


def write_array(loc, path, data, first, last, step):
    """
    Creates (as needed) and writes data to an HDF5 array, and returns a
    message (string)

    Parameters
    ----------
    loc: h5py.File or h5py.Group
        An open file handle where to start.
    path: str
        The path of the HDF5 array.
    data: var[]
        The data to be written.
    first: numpy_array<int> (or None)
        The position of the first element to be written.
    last: numpy_array<int> (or None)
        The position of the last element to be written.
    step: numpy_array<int> (or None)
        The write stride.
    """

    ret = path

    if not is_h5_location_handle(loc):
        raise TypeError('Location handle expected.')

    if not isinstance(path, str):
        raise TypeError, 'String expected.'

    # is the location valid?
    create_dset = False
    if not resolvable(loc, path):
        if not path_is_available_for_obj(loc, path, h5py.Dataset): 
            return "Unable to create an HDF5 array at '%s'." % (path)
        else:
            create_dset = True
    else:
        if loc.get(path, getclass=True) != h5py.Dataset:
            return "The object at '%s' is not an HDF5 array." % (path)

    # if the dataset doesn't exist, we're ready to roll
    if create_dset:
        try:
            loc.create_dataset(path, data.shape, dtype=data.dtype,
                               data=data)
        except Exception, e:
            print e
            logger.info(e)
            ret = 'Internal error.'
    else:

        # examine the file and memory type compatibility

        # examine the shape and hyperslab specifications
        
        pass

    return ret

#==============================================================================


@xl_func("string filename, string arrayname, var[] data, var first, var last, var step : string",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=True)
def h5writeArray(filename, arrayname, data, first, last, step):
    """
    Writes data to an HDF5 dataset

    :param filename: the name of an HDF5 file
    :param arrayname: the path name of an HDF5 array
    :param data: an Excel range of data to be written
    :param first: the (1-based) index of the first element to be written (optional)
    :param last: the (1-based) index of the last element to be written (optional)
    :param stride: the write stride in each dimension (optional)
    :returns: A string
    """

#==============================================================================

    ret = arrayname

    if not isinstance(filename, str):
        raise TypeError, "'filename' must be a string."

    if not isinstance(arrayname, str):
        raise TypeError, "'arrayname' must be a string."

    # 'data' must be a 1D or 2D array of a supported type

    if not isinstance(data, list):
        raise TypeError, "'data' must be a list."
    
    npdata = None
    try:
        npdata = np.asarray(data)
    except:
        return 'Invalid (non-array) data found.'
    if npdata.size == 0:
        return 'No data found.'
    if not is_supported_h5array_type(npdata.dtype):
        return "Unsupported element type '%s' found." % (npdata.dtype)    
    if npdata.ndim < 1 or npdata.ndim > 2:
        return 'The data range must be one- or two-dimensional.'

    # 'first' must be a 1D array of integers (or empty)
    npfirst = None
    if first is not None:
        if not isinstance(first, (float, list)):
            raise TypeError, "'first' must be an integer or integer array."
        else:
            npfirst, ret = try_intarray(first)
            if npfirst is None:
                return ret
            
    # 'last' must be a 1D array of integers (or empty)
    nplast = None
    if last is not None:
        if not isinstance(last, (float, list)):
            raise TypeError, "'last' must be an integer or integer array."
        else:
            nplast, ret = try_intarray(last)
            if nplast is None:
                return ret

    # 'step' must be a 1D array of integers (or empty)
    npstep = None
    if step is not None:
        if not isinstance(step, (float, list)):
            raise TypeError, "'step' must be an integer or integer array."
        else:
            npstep, ret = try_intarray(step)
            if npstep is None:
                return ret
    
    if filename.strip() == '':
        return 'Missing file name.'

    try:
        with h5py.File(filename, 'a') as f:
            ret = write_array(f, arrayname, npdata, npfirst, nplast, npstep)

    except IOError, e:
        logger.info(e)
        ret = "Can't open/create file '%s'." % (filename)
    except Exception, e:
        logger.info(e)
        return 'Internal error.'

    return ret
