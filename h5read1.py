
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
@xl_arg_doc("start", "The zero-based index of the first element to be read.")
@xl_arg_doc("count", "The number of elements to be read in each dimension.")

@xl_func("string filename, string datasetname, int[] start, int[] count : string",
         category="HDF5",
         thread_safe=False,
         macro=True,
         disable_function_wizard_calc=True)
def h5read1(filename, datasetname, start, count):
    """
    Reads a subset of an HDF5 dataset. The subset is described by the position,
    start, of the first element to be read and, count, the number of elements to be
    read in each dimension. For a two-dimensional dataset, start and count are
    arrays of length two.

    If the start falls outside the dataset, nothing is returned.

    If the count exceeds the number of elements in that dimension, it is
    automatically truncated.

    If the count is negative, all elements in that dimension beginning at start
    will be read.
    """

#===============================================================================

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

        start_tup = h5xl.get_tuple(start)
        count_tup = h5xl.get_tuple(count)

        # sanity check
        if len(start_tup) != len(dsp) or len(count_tup) != len(dsp):
            return 'Dataset rank mismatch in start or count.'

        for i in range(len(dsp)):
            if start_tup[i] < 0:
                return 'start entries must be non-negative.'
            # empty selection
            if start_tup[i] >= dsp[i]:
                return 'Empty selection.'
            if count_tup[i] < 0:
                count_tup[i] = dsp[i] - start_tup[i]
            if count_tup[i] == 0:
                return 'count entries must be non-zero.'
            # overflow?
            if (start_tup[i] + count_tup[i]) > dsp[i]:
                count_tup[i] = dsp[i] - start_tup[i]

        # we return the dimensions on success
        if len(dsp) == 1:
            ret = '%i x 1' % count_tup[0]
        else:
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
                        last_row = start_tup[0] + count_tup[0]
                        x = np.reshape(dset[start_tup[0]:last_row],
                                       (count_tup[0],1))
                    else:
                        range = xl.Range(range.Resize(2,2),
                                         range.Resize(count_tup[0]+1, count_tup[1]+1))
                        last_row = start_tup[0] + count_tup[0]
                        last_col = start_tup[1] + count_tup[1]
                        x = dset[start_tup[0]:last_row,start_tup[1]:last_col]
                        
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
