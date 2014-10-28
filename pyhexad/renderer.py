
import logging

import h5py
import numpy as np
import pyxll

import automation
from type_helpers import excel_dtype

logger = logging.getLogger(__name__)


def draw(x):
    """ Renders a one- or twodimensional scalar array.
    """

    if not isinstance(x, np.ndarray):
        raise TypeError('Numpy ndarray expected.')

    # get the address of the calling cell using xlfCaller
    caller = pyxll.xlfCaller()
    address = caller.address

    #=======================================================================
    # the update is done asynchronously so as not to block some
    # versions of Excel by updating the worksheet from a worksheet function
    def update_func():
        xl = automation.xl_app()
        range = xl.Range(address)
        y = None

        try:
            if x.ndim == 1:
                range = xl.Range(range.Resize(2, 1),
                                 range.Resize(x.shape[0]+1, 1))
                # we need to reshape a 1D vector into a 2D array
                y = np.reshape(x, (x.shape[0], 1))
            elif x.ndim == 2:
                range = xl.Range(range.Resize(2, 1),
                                 range.Resize(x.shape[0]+1, x.shape[1]))
                y = x
            else:
                raise ValueError('Array rank must be 1 or 2.')

            # Question: should the caller do this???
            # we can handle only strings, int32, and float64
            if y.dtype != h5py.special_dtype(vlen=str):
                range.Value = np.asarray(y, dtype=excel_dtype(y.dtype))
            else:
                range.Value = y

        except Exception, ex:
            logger.info(ex)
    #
    #=======================================================================

    # kick off the asynchronous call to the update function
    pyxll.async_call(update_func)


#==============================================================================

    
def draw_table(x):
    """
    Renders a table = list of rows = list of lists.

    We assume the CALLER did the proper type conversions!!!
    (We can handle strings, int32, and float64 colums.)
    """

    if not isinstance(x, list):
        raise TypeError('List expected.')

    # get the address of the calling cell using xlfCaller
    caller = pyxll.xlfCaller()
    address = caller.address

    #=======================================================================
    # the update is done asynchronously so as not to block some
    # versions of Excel by updating the worksheet from a worksheet function
    def update_func():
        xl = automation.xl_app()
        range = xl.Range(address)

        try:

            header = x[0]
            num_cols = len(header)
            num_rows = len(x)
            
            range = xl.Range(range.Resize(2, 1),
                             range.Resize(num_rows+1, num_cols))
            range.Value = x

        except Exception, ex:
            logger.info(ex)
    #
    #=======================================================================

    # kick off the asynchronous call to the update function
    pyxll.async_call(update_func)
