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
from table_helpers import parse_col_names

logger = logging.getLogger(__name__)

#=============================================================================


def write_rows(loc, path, rows, columns):
    """
    Write rows to an existing table and return the number of rows written.

    Parameters
    ----------
    loc: h5py.File or h5py.Group
        An open file handle where to start.
    path: str
        The path of the HDF5 table.
    rows: var[]
        The rows to be appended.
    columns: string
        A comma-separated list of column names (optional)
    """

    ret = path

    if not is_h5_location_handle(loc):
        raise TypeError('Location handle expected.')

    if not isinstance(path, str):
        raise TypeError('String expected.')

    if not isinstance(rows, list):
        raise TypeError('List expected.')

    if not isinstance(columns, str):
        raise TypeError('String expected.')

    # is the location valid?
    if not resolvable(loc, path):
        return "HDF5 table at '%s' not found." % (path)
    if loc.get(path, getclass=True) != h5py.Dataset:
        return "The object at '%s' is not an HDF5 table." % (path)

    dset = loc[path]
    file_type = dset.dtype

    # check for column names
    col_names = ()
    if columns != '':
        col_names = tuple(parse_col_names(columns))
        for c in col_names:
            if c not in file_type.names:
                return "Unknown colum name '%s' found." % (c)

    # if we have a column subset, we need to construct a reduced compound
    mem_type = file_type
    if len(col_names) > 0:
        l = []
        for c in col_names:
            l.append((c, file_type.fields[c][0]))
        mem_type = np.dtype(l)

    # try to convert the ROWS list-of-lists into a Numpy array
    a = np.zeros((len(rows),), dtype=mem_type)
    try:
        x = np.asarray(rows)

        # change the names collection as needed
        names = file_type.names if len(col_names) == 0 else col_names

        for i in range(len(rows)):
            # we assume that the columns are provided in the file order
            field_count = 0
            for fld in names:
                a[i][fld] = x[i][field_count]
                field_count += 1

    except Exception, e:
        logger.info(e)
        return "Can't convert rows to the element type in the file."

    # (if needed) extend the table and write the rows
    try:

        curr_rows = dset.shape[0]
        new_rows = len(rows)
        if new_rows > curr_rows:
            dset.resize((new_rows,))

        if len(col_names) > 0:
            idx = col_names + (slice(0, new_rows),)
            dset[idx] = a
        else:
            dset[0:new_rows] = a

        ret = "%d rows written." % (new_rows)

    except Exception, e:
        print e
        logger.info(e)
        ret = 'Write failed.'

    return ret

#=============================================================================


@xl_func("string filename, string tablename, var[] rows, string columns: var",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=True)
def h5writeTable(filename, tablename, rows, columns):
    """
    Write rows to an HDF5 table. Optionally, write only a subset of columns.

    :param filename: the name of an HDF5 file
    :param tablename: the path name of an HDF5 table
    :param rows: an Excel range of rows
    :param columns: a string, a comma separated list of column names
    :returns: A string
    """

#=============================================================================

    ret = '\0'

    if not isinstance(filename, str):
        raise TypeError("'filename' must be a string.")

    if not isinstance(tablename, str):
        raise TypeError("'tablename' must be a string.")

    if not isinstance(rows, list):
        raise TypeError("'rows' must be a list.")

    if not isinstance(columns, str):
        raise TypeError("'columns' must be a string.")

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

            ret = write_rows(f, tablename, rows, columns)

    except IOError, e:
        logger.info(e)
        ret = "Can't open/create file '%s'." % (filename)
    except Exception, e:
        logger.info(e)
        return 'Internal error.'

    return ret
