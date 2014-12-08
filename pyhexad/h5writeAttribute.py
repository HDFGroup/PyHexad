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

from h5_helpers import is_h5_location_handle, resolvable

logger = logging.getLogger(__name__)

#==============================================================================


def set_attribute(loc, path, attname, attvalue):
    """
    Creates a new HDF5 array and returns a message (string)

    Parameters
    ----------
    loc: h5py.File or h5py.Group
        An open file handle where to start.
    path: str
        The path where to the attributee.
    attname: string
        The attribute name.
    attvalue: var
        The attribute value.
    """

    ret = attname

    if not is_h5_location_handle(loc):
        raise TypeError('Location handle expected.')

    if not isinstance(path, str):
        raise TypeError('String expected.')

    if not isinstance(attname, str) or attname == '':
        raise TypeError('String expected.')

    if attname == '':
        return 'Empty attribute name.'

    if attvalue is None:
        raise ValueError('Value expected.')

    if not resolvable(loc, path):
        return "The path '%s' does not refer to an object." % (path)

    obj = loc[path]

    # determine the attribute type, at the moment (string, int, float)
    # TODO: provide an optional argument to force a certain type

    if isinstance(attvalue, (int, float)):
        if float(int(attvalue)) == float(attvalue):
            if attname in obj.attrs:
                del obj.attrs[attname]
            obj.attrs.create(attname, int(attvalue), dtype='i4')
        else:
            obj.attrs[attname] = attvalue
    else:
        obj.attrs[attname] = str(attvalue)

    return ret

#==============================================================================


@xl_func("string filename, string location, string attname, var attvalue: var",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=True)
def h5writeAttribute(filename, path, attname, attvalue):
    """
    Writes the value of an HDF5 attribute. Attributes will be created and
    overwritten as necessary.

    :param filename: the name of an HDF5 file
    :param path: the path name of an HDF5 object
    :param attname:  the name of an HDF5 attribute
    :param attvalue: the vale of the HDF5 attribute
    :returns: A string
    """

#==============================================================================

    if not isinstance(filename, str):
        raise TypeError('String expected.')

    if not isinstance(path, str):
        raise TypeError('String expected.')

    if not isinstance(attname, str):
        raise TypeError('String expected.')

    if attvalue is None:
        raise ValueError('Value expected.')

    ret = attname

    if filename.strip() == '':
        return 'Missing file name.'

    try:
        with h5py.File(filename, 'a') as f:
            ret = set_attribute(f, path, attname, attvalue)

    except IOError, e:
        logger.info(e)
        ret = "Can't open/create file '%s'." % (filename)
    except Exception, e:
        logger.info(e)
        return 'Internal error.'

    return ret
