
import pyxll
from pyxll import xl_arg_doc, xl_func, xl_macro
import h5py
import h5xl
import numpy as np

import logging
_log = logging.getLogger(__name__)

#==============================================================================

@xl_func("string filename, string datasetname, var[] data : string",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=True)
def h5writeArray(filename, datasetname, data):
    """
    Writes data to an HDF5 dataset

    :param filename: the name of an HDF5 file
    :param arrayname: the path name of an HDF5 array
    :param data: an Excel range of data to be written
    :returns: A string
    """

#==============================================================================

    ret = None

    try:
        with h5py.File(filename,'a') as f:

            if not datasetname in f: # it doesn't exist

                if not h5xl.path_is_available_for_obj(f, datasetname, h5py.Dataset):
                    return 'Unable to create dataset.'

                if not data.dtype in h5xl.supported_dtypes:
                    return "Unsupported element type in 'data'."

                if not (len(data.shape) == 2 or len(data.shape) == 1):
                    return "Unsupported shape. 1D and 2D shapes only."

                f.create_dataset(datasetname, data.shape, dtype=data.dtype,
                                             data=data)
                                                
            else: # the path name is in use
                if f.get(datasetname, getclass=True) != h5py.Dataset:
                    return "'datasetname' does not refer to an HDF5 dataset."
                dst = f[datasetname]

                # TODO: we should be a little more lenient here: if the type
                # of 'data' can be coerced, we should allow this through
                if dst.dtype != data.dtype:
                    return 'Element type mismatch.'

                # reshape if necessary
                if not h5xl.can_reshape(data, dst.shape):
                    return 'Shape mismatch.'
                else:
                    data = np.reshape(data, dst.shape)

                dst[...] = data
                
            ret = datasetname
            
    except IOError, io:
        return "Can't open or create file."
    except Exception, e:
        _log.info(e)
        ret = 'Internal error.'

    return ret
