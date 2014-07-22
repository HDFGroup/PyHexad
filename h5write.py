
import pyxll
from pyxll import xl_arg_doc, xl_func, xl_macro
import h5py
import h5xl
import numpy as np

import logging
_log = logging.getLogger(__name__)

#==============================================================================

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_arg_doc("datasetname", "The name of the dataset.")
@xl_arg_doc("data", "The data to be written.")
@xl_func("string filename, string datasetname, numpy_array data : string",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=True)
def h5write(filename, datasetname, data):
    """
    Writes data to an HDF5 dataset

    If the file doesn't exist, a new file will be created.

    h5write supports only floating-point and integer datasets.

    For exisiting datasets an error will be generated, if there is an
    element type or shape mismatch.
    """

#==============================================================================

    ret = None

    try:
        with h5py.File(filename,'r+') as f:
            ret = "I got the file."

            # get the dataset
            dst = None
            if not datasetname in f: # it doesn't exist

                if not h5xl.path_is_available_for_obj(f, datasetname, h5py.Dataset):
                    return 'Unable to create dataset.'

                if not data.dtype in h5xl.supported_dtypes:
                    return "Unsupported element type in 'data'."

                if len(data.shape) == 2 or len(data.shape) == 1:
                    return "Usupported shape. 1D and 2D shapes only."

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
                if dst.shape != data.shape:
                    return 'Shape mismatch.'

                dst[...] = data
                
            ret = datasetname
            
    except IOError, io:
        return "Can't open or create file."
    except Exception, e:
        _log.info(e)
        ret = 'Internal error.'

    return ret
