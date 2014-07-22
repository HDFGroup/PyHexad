
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
@xl_arg_doc("first", "The (one-based) index of the first element to be written.")
@xl_arg_doc("last", "The (one-based) index of the last elements to be written.")

@xl_func("string filename, string datasetname, numpy_array data, int[] first, int[] last : string",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=True)
def h5write1(filename, datasetname, data, first, last):
    """
    Writes data to a subset of an HDF5 dataset. The subset is described by the
    position, 'first', of the first element to be written and, 'last', the
    position of the last element to be written.
    For a two-dimensional dataset, first and last are arrays of length two.

    The positions of elements are 1-based, i.e., begin at 1 and end
    at the extent of the respective dimension.

    If 'first' falls outside the dataset, nothing is written.

    If 'last' is beyond the last position of elements, an error is generated.
    
    If the file or dataset doesn't exist, an error is generated.

    An error  will be generated, in case of an element type or shape mismatch.
    """

#==============================================================================

    ret = None

    try:
        with h5py.File(filename,'r+') as f:

            if (not datasetname in f) or (f.get(datasetname, getclass=True) != h5py.Dataset):
                return "Can't find dataset."

            dst = f[datasetname]

            # check the dataset type and shape against the hyperslab
            
            # TODO: we should be a little more lenient here: if the type
            # of 'data' can be coerced, we should allow this through
            if dst.dtype != data.dtype:
                return 'Element type mismatch.'
                
            first_tup = h5xl.get_tuple(first)
            last_tup = h5xl.get_tuple(last)

            dsp = dst.shape

            # rank check
            if len(first_tup) != len(last_tup):
                return "Rank mismatch between 'first' and 'last'."

            # convert to Numpy indexing
            start = [(i-1) for i in first_tup]
            stop = [i for i in last_tup]

            for i in range(len(dsp)):
                if start[i] < 0:
                    return "'first' entries must be positive."
                # empty selection
                if start[i] >= dsp[i]:
                    return 'Empty selection.'
                if stop[i] <= 0:
                    return "'last' entries must be positive."
                # overflow?
                if stop[i] > dsp[i]:
                    stop[i] = dsp[i]
                # final check
                if stop[i] <= start[i]:
                    return "'last' entries must be greater or equal than 'first'."

            start_tup = tuple(start)
            stop_tup = tuple(stop)
            count_tup = None

            # we return the dimensions on success
            if len(dsp) == 1:
                count_tup = (stop_tup[0]-start_tup[0], 1)
                ret = '%i x 1' % (count_tup[0])
            else:
                count_tup = (stop_tup[0]-start_tup[0], stop_tup[1]-start_tup[1])
                ret = "%i x %i" % (count_tup[0], count_tup[1])

            if not h5xl.can_reshape(data, count_tup):
                return "The data array does not fit the dataset selection."
            else:
                data = np.reshape(data, count_tup)

            dst[start_tup[0]:stop_tup[0],start_tup[1]:stop_tup[1]] = data
                            
    except IOError, io:
        return "Can't open file."
    except Exception, e:
        _log.info(e)
        ret = 'Internal error.'

    return ret
