
import automation
import file_helpers
from file_helpers import file_exists
import h5py
import logging
import numpy as np
import pyxll
from pyxll import xl_arg_doc, xl_func
import type_helpers
from type_helpers import is_supported_h5array_type, excel_dtype

_log = logging.getLogger(__name__)

#===============================================================================

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_arg_doc("arrayname", "The name of the HDF5 array.")
@xl_func("string filename, string arrayname : string",
         category="HDF5",
         thread_safe=False,
         macro=True,
         disable_function_wizard_calc=True)
def h5readArray(filename, arrayname):
    """
    Reads an HDF5 array
    """

#===============================================================================

    ret = '\0'

    if not isinstance(filename, str):
        return "'filename' must be a string."

    if not isinstance(arrayname, str):
        return "'arrayname' must be a string."
            
    if not file_exists(filename):
        return "Can't open file."

    with h5py.File(filename, 'r') as f:

        # do we have a dataset?
        if (not arrayname in f) or (f.get(arrayname, getclass=True) != h5py.Dataset):
            return "Can't open dataset."
        dst = f[arrayname]

        # is it the right shape?
        dsp = dst.shape
        if (len(dsp) < 1) or (len(dsp) > 2):
            return "Unsupported dataset shape."

        # has it the right type?
        dty = dst.dtype
        if not is_supported_h5array_type:
            return "Unsupported dataset element type."
            
        # get the address of the calling cell using xlfCaller
        caller = pyxll.xlfCaller()
        address = caller.address

        # we return the dimensions on success
        if len(dsp) == 1:
            ret = '%i x 1' % dsp[0]
        else:
            ret = "%i x %i" % (dsp[0], dsp[1])
        
        # the update is done asynchronously so as not to block some
        # versions of Excel by updating the worksheet from a worksheet function
        def update_func():
            xl = automation.xl_app()
            range = xl.Range(address)
            rows = xl.Range(address)
            cols = xl.Range(address)
            
            try:
                with h5py.File(filename, 'r') as f:
                    dset = f[arrayname]
                    mty = excel_dtype(dst.dtype)

                    x = None
                    
                    # we can handle only 1D or 2D datasets
                    if len(dset.shape) == 1:
                        range = xl.Range(range.Resize(2,2),
                                         range.Resize(dsp[0]+1,2))
                        x = np.reshape(dset[...], (dsp[0],1))
                    else:
                        range = xl.Range(range.Resize(2,2),
                                         range.Resize(dsp[0]+1, dsp[1]+1))
                        x = dset[...]
                        
                        # print the number of columns
                        cols = xl.Range(rows.Resize(3,1),rows.Resize(3,1))
                        cols.Value = dsp[1]
                            
                    range.Value = np.asarray(x, dtype=mty)

                    # this looks awkward. there must be a better way...
                    rows = xl.Range(rows.Resize(2,1),rows.Resize(2,1))
                    rows.Value = dsp[0]
                    
            except Exception, ex:
                _log.info(ex)
                ret = 'Internal error.'

        # kick off the asynchronous call to the update function
        pyxll.async_call(update_func)

        return ret
