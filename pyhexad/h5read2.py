
import automation
import pyxll
from pyxll import xl_arg_doc, xl_func
import h5py
import h5xl
import numpy as np

import logging
_log = logging.getLogger(__name__)

#===============================================================================

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_arg_doc("datasetname", "The name of the dataset.")
@xl_arg_doc("first", "The (one-based) index of the first element to be read.")
@xl_arg_doc("last", "The (one-based) index of the last elements to be read.")
@xl_arg_doc("step", "The read stride in each dimension.")

@xl_func("string filename, string datasetname, int[] first, int[] last, int[] step : string",
         category="HDF5",
         thread_safe=False,
         macro=True,
         disable_function_wizard_calc=True)
def h5read2(filename, datasetname, first, last, step):
    """
    Reads a subset of an HDF5 dataset. The subset is described by the position,
    'first', of the first element to be read, 'last', the position of the last
    element to be read, and, 'step', the read stride.
    For a two-dimensional dataset, 'first', 'last', and 'step' are arrays
    of length two.

    The positions of elements are 1-based, i.e., begin at 1 and end
    at the extent of the respective dimension.

    If 'first' falls outside the dataset, nothing is returned.

    If 'last' is beyond the last position of elements, it is automatically
    adjusted to the last position.

    If the 'last' is negative, all elements in that dimension beginning at
    'start' will be read.

    The elements of 'step' must be positive.
    """

#===============================================================================

    if not isinstance(filename, str):
        raise TypeError, 'String expected.'
        
    if not isinstance(datasetname, str):
        raise TypeError, 'String expected.'

    if not isinstance(first, list):
        raise TypeError, 'List expected.'
        
    if not isinstance(last, list):
        raise TypeError, 'List expected.'
        
    if not isinstance(step, list):
        raise TypeError, 'List expected.'

    ret = None
    
    if not h5xl.file_exists(filename):
        return "Can't open file."

    with h5py.File(filename, 'r') as f:

        # do we have a dataset?
        if (not datasetname in f) or (f.get(datasetname, getclass=True) != h5py.Dataset):
            return "Can't open dataset."
        dst = f[datasetname]

        # is it the right shape?
        dsp = dst.shape
        if (len(dsp) < 1) or (len(dsp) > 2):
            return "Unsupported dataset shape."

        # has it the right type?
        dty = dst.dtype
        if dty not in h5xl.supported_dtypes:
            return "Unsupported dataset element type."

        # get the address of the calling cell using xlfCaller
        caller = pyxll.xlfCaller()
        address = caller.address

        first_tup = h5xl.get_tuple(first)
        last_tup = h5xl.get_tuple(last)
        step_tup = h5xl.get_tuple(step)

        # sanity check
        if len(first_tup) != len(dsp) or len(last_tup) != len(dsp) or len(step_tup) != len(dsp):
            return "Dataset rank mismatch in 'first', 'last', or 'step'."

        # convert to Numpy indexing
        start = [(i-1) for i in first_tup]
        stop = [i for i in last_tup]
        step = [i for i in step_tup]
            
        for i in range(len(dsp)):
            if start[i] < 0:
                return "'first' entries must be positive."
            # empty selection
            if start[i] >= dsp[i]:
                return 'Empty selection.'
            if stop[i] < 0:
                stop[i] = dsp[i]
            # overflow?
            if stop[i] > dsp[i]:
                stop[i] = dsp[i]
            # final check
            if stop[i] <= start[i]:
                return "'last' entries must be greater or equal than 'first'."
            if step[i] < 1:
                return "'step' entries must be positive (>= 1)."

        start_tup = tuple(start)
        stop_tup = tuple(stop)
        step_tup = tuple(step)
        count_tup = None
        
        # we return the dimensions on success
        if len(dsp) == 1:
            cnt = (stop_tup[0]-start_tup[0])/step_tup[0]
            if cnt > 0:
                count_tup = (cnt, 1)
            else:
                count_tup = (1, 1)
        else:
            rows = (stop_tup[0]-start_tup[0])/step_tup[0]
            if rows == 0: rows = 1
            cols = (stop_tup[1]-start_tup[1])/step_tup[1]
            if cols == 0: cols = 1
            count_tup = (rows, cols)
            
        ret = "%i x %i" % (count_tup[0], count_tup[1])

        # the update is done asynchronously so as not to block some
        # versions of Excel by updating the worksheet from a worksheet function
        def update_func():
            xl = automation.xl_app()
            range = xl.Range(address)
            rows = xl.Range(address)
            cols = xl.Range(address)
            
            try:
                with h5py.File(filename, 'r') as f:
                    dset = f[datasetname]
                    x = None
                    
                    # we can handle only 1D or 2D datasets
                    if len(dset.shape) == 1:
                        range = xl.Range(range.Resize(2,2),
                                         range.Resize(count_tup[0]+1,2))
                        x = np.reshape(dset[start_tup[0]:stop_tup[0]:step[0]],
                                       (count_tup[0],1))
                    else:
                        range = xl.Range(range.Resize(2,2),
                                         range.Resize(count_tup[0]+1, count_tup[1]+1))
                        x = dset[start_tup[0]:stop_tup[0]:step[0],
                                 start_tup[1]:stop_tup[1]:step[1]]
                        
                        # print the number of columns
                        cols = xl.Range(rows.Resize(3,1),rows.Resize(3,1))
                        cols.Value = count_tup[1]
                            
                    range.Value = np.asarray(x, dtype=np.float64)

                    # this looks awkward. there must be a better way...
                    rows = xl.Range(rows.Resize(2,1),rows.Resize(2,1))
                    rows.Value = count_tup[0]
                    
            except Exception, ex:
                _log.info(ex)

        # kick off the asynchronous call to the update function
        pyxll.async_call(update_func)

        return ret