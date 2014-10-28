
import logging

import h5py
from pyxll import xl_func

from file_helpers import file_exists
from h5_helpers import path_is_valid_wrt_loc
from renderer import draw_table
from type_helpers import excel_dtype, is_supported_h5table_type 

logger = logging.getLogger(__name__)

#==============================================================================


def get_table(loc, path, columns, first=None, last=None, step=None):
    """
    Returns a tuple of a list of rows (lists) and an error message.
    """

    # Is this a valid location?
    is_valid, species = path_is_valid_wrt_loc(loc, path)
    if not is_valid:
        return (None, 'Invalid location specified.')

    # Do we have a dataset?
    if (loc.get(path) is None) or \
       (loc.get(path, getclass=True) != h5py.Dataset):
        return (None, "Can't open HDF5 table '%s'." % (path))

    dset = loc[path]

    # Does it have the right shape?
    dsp = dset.shape
    if len(dsp) != 1:
        return (None, 'This is not an HDF5 table.')

    # Does it have the right type?
    file_type = dset.dtype
    if not is_supported_h5table_type(file_type):
        return (None, 'Unsupported HDF5 table type.')

    # upgrade everything to string, int32, or float64
    mem_type = excel_dtype(file_type)

    # Is the column selection meaningful?

    col_names = None
    if columns is not None:
        for c in columns:
            if c[0] not in file_type.names:
                return (None, "Unknown column '%s'." % (c))
        col_names = [c[0] for c in columns]
    else:
        col_names = [n for n in mem_type.names]

    # Is the hyperslab selection meaningful?
    # The hyperslab selection is 1-based => Convert it to 0-based notation.

    start = 0     if first is None else first-1
    stop = dsp[0] if last  is None else last
    stride = 1    if step  is None else step

    if start > stop:
        return (None, 'Empty hyperslab selection.')

    slc = slice(start, stop, stride)

    y = [col_names]
    with dset.astype(mem_type):
        if columns is not None:
            x = dset[slc]
        else:
            x = dset[slc]
        
        for r in x:
            y.append(r)

    return (y, '%d rows' % (len(y)-1))

#==============================================================================


@xl_func("string filename, string tablename, var columns, var first, var last, var step : string",
         category="HDF5",
         thread_safe=False,
         macro=True,
         disable_function_wizard_calc=True)
def h5readTable(filename, tablename, columns, first=-1, last=-1, step=-1):
    """
    Reads rows from an HDF5 table. Specify a subset of columns or a (strided)
    subset via 'first' and 'last' ('stride').

    :param filename: the name of an HDF5 file
    :param tablename: the name of an HDF5 table
    :param colums: a list of column names to be read (optional)
    :param first: the (1-based) index of the first element to be read (optional)
    :param last: the (1-based) index of the last element to be read (optional)
    :param stride: the read stride in each dimension (optional)
    :returns: A string
    """

#===============================================================================

    ret = '\0'

    # sanity check

    if not isinstance(filename, str):
        return "'filename' must be a string."
    if not file_exists(filename):
        return "Can't open file '%s' or the file is not an HDF5 file." %  \
            (filename)

    if not isinstance(tablename, str):
        return "'tablename' must be a string."

    if columns is not None:
        print type(columns)
        if not isinstance(columns, list):
            return "'columns' must be a string array."
        else:
            for s in columns:
                if not isinstance(s[0], basestring):
                    return "'columns' must be a string array."

    if first is not None:
        if not (isinstance(first, float) and int(first) >= 0):
            return "'first' must be a non-negative integer."

    if last is not None:
        if not (isinstance(last, float) and int(last) >= 0):
            return "'last' must be a non-negative integer."

    if step is not None:
        if not (isinstance(step, float) and int(step) > 0):
            return "'step' must be a positive integer."

    with h5py.File(filename, 'r') as f:

        x, ret = get_table(f, tablename, columns,
                           int(first) if first is not None else None,
                           int(last)  if last  is not None else None,
                           int(step)  if step  is not None else None)
        print ret
        draw_table(x)

    return ret
