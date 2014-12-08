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

import h5py


def file_exists(filename):
    """
    Check if filename refers to an HDF5 file
    """

    if not isinstance(filename, str):
        raise TypeError('String expected.')

    result = False
    try:
        result = h5py.h5f.is_hdf5(filename)
    except Exception:
        pass
    return result
