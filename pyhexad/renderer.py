# TODO: add type and shape checking, list conversion

import automation
import logging
import numpy as np
import pyxll

_log = logging.getLogger(__name__)

def draw(x):

    if not isinstance(x, np.ndarray):
        raise TypeError, 'Numpy ndarray expected.'

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
            range = xl.Range(range.Resize(2,1),
                             range.Resize(x.shape[0]+1, x.shape[1]))
            range.Value = x

        except Exception, ex:
            _log.info(ex)
            ret = 'Internal error.'
    #
    #=======================================================================

    # kick off the asynchronous call to the update function
    pyxll.async_call(update_func)
