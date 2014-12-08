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

import h5py
import numpy as np
from pyxll import xl_func

from file_helpers import file_exists
from h5_helpers import path_is_valid_wrt_loc
import renderer
from shape_helpers import is_valid_hyperslab_spec, lol_2_ndarray
from type_helpers import excel_dtype, is_supported_h5array_type

logger = logging.getLogger(__name__)

#==============================================================================


def get_ndarray(loc, path, first=None, last=None, step=None):
    """
    Returns a tuple with the Numpy ndarray and an error message.
    """

    # Is this a valid location?
    is_valid, species = path_is_valid_wrt_loc(loc, path)
    if not is_valid:
        return (None, 'Invalid location specified.')

    # Do we have a dataset?
    if (loc.get(path) is None) or \
       (loc.get(path, getclass=True) != h5py.Dataset):
        return (None, "Can't open HDF5 array '%s'." % (path))

    dst = loc[path]

    # Does it have the right shape?
    # TODO: how does h5py represent NULL dataspaces?
    dsp = dst.shape
    if len(dsp) > 2:
        return (None, 'Unsupported dataset shape.')

    # Does it have the right type?
    file_type = dst.dtype
    if not is_supported_h5array_type(file_type):
        return None, 'Unsupported dataset element type.'

    # upgrade everything to string, int32, or float64
    mem_type = excel_dtype(file_type)

    rk = len(dsp)

    # Is the hyperslab selection meaningful?
    if rk != 0:
        if not is_valid_hyperslab_spec(np.asarray(dsp), first, last, step):
            return None, 'Invalid hyperslab specification.'

    # The hyperslab selection is 1-based => Convert it to 0-based notation.
    if rk == 0:
        x = np.asarray([dst[()]])
        return(x, '1 x 1')

    elif rk == 1:

        start = 0 if first is None else first[0]-1
        stop = dsp[0] if last is None else last[0]
        stride = 1 if step is None else step[0]

        slc = slice(start, stop, stride)

        with dst.astype(mem_type):
            x = dst[slc]
            return (x, '%d x 1' % x.size)

    elif rk == 2:

        start = [0, 0] if first is None else [first[0]-1, first[1]-1]
        stop = [dsp[0], dsp[1]] if last is None else [last[0], last[1]]
        stride = [1, 1] if step is None else [step[0], step[1]]

        slc0 = slice(start[0], stop[0], stride[0])
        slc1 = slice(start[1], stop[1], stride[1])

        with dst.astype(mem_type):
            x = dst[slc0, slc1]
            return (x, '%d x %d' % (x.shape[0], x.shape[1]))

    else:
        return (None, 'Unsupported HDF5 array rank.')

#==============================================================================


@xl_func("string filename, string arrayname, var first, var last, var step : string",
         category="HDF5",
         thread_safe=False,
         macro=True,
         disable_function_wizard_calc=True)
def h5readArray(filename, arrayname, first, last, step):
    """
    Reads elements of an HDF5 array. Specify a rectilinear (strided) subregion
    via 'first' and 'last' ('stride').

    :param filename: the name of an HDF5 file
    :param arrayname: the name of an HDF5 array
    :param first: the (1-based) index of the first element to be read (optional)
    :param last: the (1-based) index of the last element to be read (optional)
    :param stride: the read stride in each dimension
    :returns: A string
    """

#==============================================================================

    # sanity check

    if not isinstance(filename, str):
        return "'filename' must be a string."
    if not file_exists(filename):
        return "Can't open file '%s' or the file is not an HDF5 file." %  \
            (filename)

    if not isinstance(arrayname, str):
        return "'arrayname' must be a string."

    # we get the hyperslab spec. arguments as list of lists
    # => for simplicity, convert to Numpy arrays

    ndfirst = None
    if first is not None:
        if not isinstance(first, list):
            return "'first' must be an integer array."
        else:
            ndfirst, ret = lol_2_ndarray(first)
            if ndfirst is None:
                return ret

    ndlast = None
    if last is not None:
        if not isinstance(last, list):
            return "'last' must be an integer array."
        else:
            ndlast, ret = lol_2_ndarray(last)
            if ndlast is None:
                return ret

    ndstep = None
    if step is not None:
        if not isinstance(step, list):
            return "'step' must be an integer array."
        else:
            ndstep, ret = lol_2_ndarray(step)
            if ndstep is None:
                return ret

    with h5py.File(filename, 'r') as f:

        x, ret = get_ndarray(f, arrayname, ndfirst, ndlast, ndstep)

        if x is not None:
            renderer.draw(x)

    return ret
