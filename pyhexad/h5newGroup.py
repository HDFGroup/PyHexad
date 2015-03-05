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
from pyxll import xl_func

from h5_helpers import is_h5_location_handle, path_is_available_for_obj

logger = logging.getLogger(__name__)

#==============================================================================


def new_group(loc, path):
    """
    Creates a new HDF5 group and returns a message (string)

    Parameters
    ----------
    loc: h5py.File or h5py.Group
        An open file handle where to start.
    path: str
        the path where to create the new group.
    """

    if not is_h5_location_handle(loc):
        raise TypeError('Location handle expected.')

    # check if the group already exists
    try:
        if (loc.get(path, getclass=True) == h5py.Group):
            return path
    except RuntimeError, KeyError: # h5py throws a KeyError for a dangling link
        pass

    # check if the path is available

    if path_is_available_for_obj(loc, path, h5py.Group):
        loc.require_group(path)
        return path
    else:
        return "Can't create group at '%s'." % (path)

#==============================================================================


@xl_func("string filename, string groupname: string",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=False)
def h5newGroup(filename, groupname):
    """
    Creates an HDF5 group (and missing intermediate groups or the file)

    :param filename: the name of an HDF5 file
    :param groupname: the name of the HDF5 group to be created
    :returns: A string
    """

#==============================================================================

    # sanity check

    if not isinstance(filename, str):
        raise TypeError("'filename' must be a string.")
    if not isinstance(groupname, str):
        raise TypeError("'groupname' must be a string.")

    ret = '\0'

    if filename.strip() == '':
        return 'Missing file name.'

    try:
        with h5py.File(filename, 'a') as f:
            ret = new_group(f, groupname)

    except IOError, e:
        logger.info(e)
        ret = "Can't open/create file '%s'." % (filename)
    except Exception, e:
        logger.info(e)
        return "Internal error."

    return ret
