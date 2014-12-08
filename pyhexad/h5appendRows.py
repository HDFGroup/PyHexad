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

from h5_helpers import is_h5_location_handle, resolvable

logger = logging.getLogger(__name__)

#=============================================================================


def append_rows(loc, path, rows):
    """
    Append rows to an existing table and returns the number of appended rows. 

    Parameters
    ----------
    loc: h5py.File or h5py.Group
        An open file handle where to start.
    path: str
        The path of the HDF5 table.
    rows: var[]
        The rows to be appended.

    """

    ret = path

    if not is_h5_location_handle(loc):
        raise TypeError('Location handle expected.')

    if not isinstance(path, str):
        raise TypeError('String expected.')

    if not isinstance(rows, list):
        raise TypeError('List expected.')

    # is the location valid?
    if not resolvable(loc, path):
        return "HDF5 table at '%s' not found." % (path)
    if loc.get(path, getclass=True) != h5py.Dataset:
        return "The object at '%s' is not an HDF5 table." % (path)
    
    dset = loc[path]
    file_type = dset.dtype

    # try to convert the ROWS list-of-lists into a Numpy array
    
    a = np.zeros((len(rows),), dtype=file_type)
    try:
        x = np.asarray(rows)
        for i in range(len(rows)):
            # we assume that the columns are provided in the file order
            field_count = 0
            for fld in file_type.names:
                a[i][fld] = x[i][field_count]
                field_count += 1
                
    except Exception, e:
        logger.info(e)
        return "Can't convert rows to the element type in the file."

    # extend the table and write the new rows
    
    try:

        curr_rows = dset.shape[0]
        new_rows = len(rows)

        dset.resize((curr_rows + new_rows,))
        dset[curr_rows:] = a

        ret = "%d rows appended." % (new_rows)

    except Exception, e:
        print e
        logger.info(e)
        ret = 'Write failed.'

    return ret

#=============================================================================


@xl_func("string filename, string tablename, var[] rows: var",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=True)
def h5appendRows(filename, tablename, rows):
    """
    Appends rows to an exisiting HDF5 table.

    :param filename: the name of an HDF5 file
    :param tablename: the path name of an HDF5 table
    :param rows: an Excel range of rows
    :returns: A string, the number of rows appended
    """

#=============================================================================

    ret = '\0'

    if not isinstance(filename, str):
        raise TypeError("'filename' must be a string.")

    if not isinstance(tablename, str):
        raise TypeError("'tablename' must be a string.")

    try:

        with h5py.File(filename, 'a') as f:

            # does the table exist?
            if not resolvable(f, tablename):
                return 'Table not found.'
            
            # is it a dataset?
            if f.get(tablename, getclass=True) != h5py.Dataset:
                return "The object at '%s' is not an HDF5 table." % \
                    (tablename)

            # is it a table shape?
            dset = f[tablename]
            if len(dset.shape) != 1 or dset.maxshape != (None,):
                return "The object at '%s' is not an HDF5 table." % \
                    (tablename)

            # is it a table type?
            if dset.dtype.names is None:
                return "The object at '%s' is not an HDF5 table." % \
                    (tablename)

            ret = append_rows(f, tablename, rows)

    except IOError, e:
        logger.info(e)
        ret = "Can't open/create file '%s'." % (filename)
    except Exception, e:
        logger.info(e)
        return 'Internal error.'

    return ret
