##############################################################################
# Copyright by The HDF Group.                                                #
# All rights reserved.                                                       #
#                                                                            #
# This file is part of PyHexad. The full PyHexad copyright notice, including #
# terms governing use, modification, and redistribution, is contained in     #
# the file COPYING, which can be found at the root of the source code        #
# distribution tree.  If you do not have access to this file, you may        #
# request a copy from help@hdfgroup.org.                                     #
##############################################################################

import logging

logger = logging.getLogger(__name__)

try:
    import win32com.client
except ImportError:
    logger.warning("*** win32com.client could not be imported          ***")
    logger.warning("*** some of the automation examples will not work  ***")
    logger.warning("*** to fix this, install the pywin32 extensions.   ***")

import numpy as np
import pyxll

#==============================================================================

def xl_app():
    """returns a Dispatch object for the current Excel instance"""
    # get the Excel application object from PyXLL and wrap it
    xl_window = pyxll.get_active_object()
    xl_app = win32com.client.Dispatch(xl_window).Application
    # it's helpful to make sure the gen_py wrapper has been created
    # as otherwise things like constants and event handlers won't work.
    win32com.client.gencache.EnsureDispatch(xl_app)
    
    return xl_app

#==============================================================================


def draw(arr):
    """Renders a one- or twodimensional scalar array."""

    if not isinstance(arr, np.ndarray):
        raise TypeError('Numpy ndarray expected.')

    # get the address of the calling cell using xlfCaller
    caller = pyxll.xlfCaller()
    address = caller.address
    
    #=======================================================================
    # the update is done asynchronously so as not to block some
    # versions of Excel by updating the worksheet from a worksheet function
    def update_func(x):

        xl = xl_app()

        if xl is not None:
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

                range.Value = y

            except Exception, ex:
                logger.info(ex)
    #
    #=======================================================================

    # kick off the asynchronous call to the update function
    pyxll.async_call(update_func, arr)


#==============================================================================


def draw_table(tbl):
    """
    Renders a table = list of rows = list of lists.

    We assume the CALLER did the proper type conversions!!!
    (We can handle strings, int32, and float64 colums.)
    """

    if not isinstance(tbl, list):
        raise TypeError('List expected.')

    # get the address of the calling cell using xlfCaller
    caller = pyxll.xlfCaller()
    address = caller.address

    #=======================================================================
    # the update is done asynchronously so as not to block some
    # versions of Excel by updating the worksheet from a worksheet function
    def update_func(x):

        xl = xl_app()

        if xl is not None:
            range = xl.Range(address)

            try:

                header = x[0]
                num_cols = len(header)
                num_rows = len(x)

                range = xl.Range(range.Resize(2, 1),
                                 range.Resize(num_rows + 1, num_cols))
                range.Value = x

            except Exception, ex:
                logger.info(ex)
    #
    #=======================================================================

    # kick off the asynchronous call to the update function
    pyxll.async_call(update_func, tbl)
