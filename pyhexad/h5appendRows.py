
import logging

import h5py
import numpy as np
from pyxll import xl_func

from h5_helpers import is_h5_location_handle, resolvable

logger = logging.getLogger(__name__)

#=============================================================================


@xl_func("string filename, string tablename, var[] rows: var",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=True)
def h5appendRows(filename, tablename, rows):
    """
    Appends rows to an HDF5 table.

    :param filename: the name of an HDF5 file
    :param tablename: the path name of an HDF5 table
    :param rows: an Excel range of rows
    :returns: A string
    """

#=============================================================================

    return 0
