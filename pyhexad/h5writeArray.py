
import logging

import h5py
import h5xl
import numpy as np
import pyxll
from pyxll import xl_func

from h5_helpers import is_h5_location_handle, path_is_available_for_obj, \
    resolvable
from shape_helpers import try_intarray, can_reshape
from type_helpers import is_supported_h5array_type

logger = logging.getLogger(__name__)

#==============================================================================


def create_array(loc, path, data):
    """
    Creates and writes data to an HDF5 array, and returns a
    message (string)

    Parameters
    ----------
    loc: h5py.File or h5py.Group
        An open file handle where to start.
    path: str
        The path of the HDF5 array.
    data: var[]
        The data to be written.
    """

    ret = path

    if not is_h5_location_handle(loc):
        raise TypeError('Location handle expected.')

    if not isinstance(path, str):
        raise TypeError, 'String expected.'

    if not path_is_available_for_obj(loc, path, h5py.Dataset): 
        return "Unable to create an HDF5 array at '%s'." % (path)
  
    try:
        file_type = data.dtype
        # store strings in UTF-8 encoding
        if file_type.char in ('S', 'U'):
            file_type = h5py.special_dtype(vlen=unicode)

        loc.create_dataset(path, data.shape, dtype=file_type,
                           data=data.astype(file_type))
    except Exception, e:
        logger.info(e)
        print e
        ret = 'Array creation faild.'
            
    return ret

#==============================================================================


def write_array(loc, path, data, slice_tuple):
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
    slice_tuple: tuple of slices
        The destination indices to be written.
    """

    ret = path

    if not is_h5_location_handle(loc):
        raise TypeError('Location handle expected.')

    if not isinstance(path, str):
        raise TypeError, 'String expected.'

    # is the location valid?
    if not resolvable(loc, path):
        return "HDF5 array at '%s' not found." % (path)
    if loc.get(path, getclass=True) != h5py.Dataset:
        return "The object at '%s' is not an HDF5 array." % (path)

    dset = loc[path]
    file_type = dset.dtype
    try:
        x = data.astype(file_type)
    except:
        return "Can't convert data to element type in the file."

    try:

        rk = len(dset.shape)
        rshape = tuple([(slice_tuple[i].stop-slice_tuple[i].start)/ \
                        slice_tuple[i].step for i in range(rk)])
        dset[slice_tuple] = data.reshape(rshape).astype(file_type)

    except Exception, e:
        print e
        logger.info(e)
        ret = 'Write failed.'

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
    :param step: the write stride in each dimension (optional)
    :returns: A string
    """

#==============================================================================

    ret = arrayname

    if not isinstance(filename, str):
        raise TypeError, "'filename' must be a string."

    if not isinstance(arrayname, str):
        raise TypeError, "'arrayname' must be a string."

    try:
        
        with h5py.File(filename, 'a') as f:
            
            # does the array exist?
            create = False
            if not resolvable(f, arrayname):
                if not path_is_available_for_obj(f, arrayname, h5py.Dataset): 
                    return "Unable to create an HDF5 array at '%s'." % (arrayname)
                else:
                    create = True
            else:
                if f.get(arrayname, getclass=True) != h5py.Dataset:
                    return "The object at '%s' is not an HDF5 array." % (arrayname)


            # if the array doesn't exist, we can ignore the optional parameters
            # and are ready to roll
            if create:
                ret = create_array(f, arrayname, data)
                
            else:  # more checking...

                dset = f[arrayname]
                
                # normalize the optional parameters and try to write
                start = normalize_first(first, dset.shape)
                stop = normalize_last(last, dset.shape)
                stride = normalize_step(step, dset.shape)
                slc = [slice(start[i], stop[i], step[i]) for i in range(len(start))] 

                ret = write_array(f, arrayname, data, tuple(slc))

    except IOError, e:
        logger.info(e)
        ret = "Can't open/create file '%s'." % (filename)
    except Exception, e:
        logger.info(e)
        return 'Internal error.'

    return ret
