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

from h5_helpers import is_h5_location_handle, path_is_available_for_obj
from shape_helpers import get_chunk_dimensions, get_dimensions
from type_helpers import parse_dtype

logger = logging.getLogger(__name__)

#==============================================================================


def new_array(loc, path, size, plist=''):
    """
    Creates a new HDF5 array and returns a message (string)

    Parameters
    ----------
    loc: h5py.File or h5py.Group
        An open file handle where to start.
    path: str
        The path where to create the new array.
    size: list of lists
        The dimensions of the new array.
    plist: string
        A list of dataset creation properties.
    """

    ret = path

    if not is_h5_location_handle(loc):
        raise TypeError('Location handle expected.')

    # check if the path is available
    if not path_is_available_for_obj(loc, path, h5py.Dataset):
        return "Can't create array at '%s'." % (path)

    # parse the property list
    plist_ht = {}
    if plist.strip() != '':
        if len(plist.split(',')) % 2 != 0:
            return 'Invalid property list.'
        # convert the property list into a hashtable
        a = plist.split(',')
        for i in range(0, len(a), 2):
            plist_ht[a[i].strip().upper()] = a[i+1].strip()

    try:

        kwargs = {}
                
        # get shape
        dims, maxdims = get_dimensions(size)
        if dims is None:
            return 'Invalid dimensions specified.'
        kwargs['shape'] = tuple(dims)
        kwargs['maxshape'] = tuple(maxdims)

        # assemble property list

        # get type, default is float64
        file_type = np.dtype('double')
        if 'DATATYPE' in plist_ht.keys():
            try:
                file_type = parse_dtype(plist_ht['DATATYPE'].upper())
            except:
                return "Unsupported datatype '%s'." % \
                    (plist_ht['DATATYPE'].upper())
        kwargs['dtype'] = file_type

        # chunking?
        if 'CHUNKSIZE' in plist_ht.keys():
            chunk = plist_ht['CHUNKSIZE']
            chunkdims = get_chunk_dimensions(chunk)
            if chunkdims is None:
                return 'Invalid chunk dimensions specified.'
            if len(chunkdims) != len(dims):
                return 'Chunk rank must equal array rank.'
            kwargs['chunks'] = chunkdims

        # deflate?
        if 'DEFLATE' in plist_ht.keys():
            lvl = plist_ht['DEFLATE']
            try:
                lvl = int(lvl)
                if lvl < 0 or lvl > 9:
                    return 'Compression level out of range [0-9].'
                kwargs['compression'] = lvl
            except:
                return 'Invalid compression level ([0-9]).'

        # fill value
        if 'FILLVALUE' in plist_ht.keys():
            fv = plist_ht['FILLVALUE']
            try:
                if file_type in np.sctypes['float']:
                    fv = float(fv)
                elif file_type in np.sctypes['int'] or \
                file_type in np.sctypes['uint']:
                    fv = int(fv)
                kwargs['fillvalue'] = fv
            except:
                return 'Invalid fill value.'

        # Fletcher32 check sum
        if 'FLETCHER32' in plist_ht.keys():
            bool = plist_ht['FLETCHER32']
            if bool.strip().lower() == 'true':
                kwargs['fletcher32'] = True

        # Shuffle
        if 'SHUFFLE' in plist_ht.keys():
            bool = plist_ht['SHUFFLE']
            if bool.strip().lower == 'true':
                kwargs['shuffle'] = True

        # showtime!
        loc.create_dataset(path, **kwargs)

    except Exception, e:
        logger.info(e)
        ret = 'Internal error.'

    return ret

#==============================================================================


@xl_func("string filename, string datasetname, int[] size, string plist : string",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=True)
def h5newArray(filename, arrayname, size, properties):
    """
    Creates a new multi-diensional HDF5 dataset of a scalar datatype.

    :param filename: the name of an HDF5 file
    :param arrayname: the name of the HDF5 array to be created
    :param size: the dimensions of the dataset to be created
    :param properties: a list of dataset creation properties (optional)
    :returns: A string
    """
#==============================================================================

    if not isinstance(filename, str):
        return "'filename' must be a string."

    if not isinstance(arrayname, str):
        return "'arrayname' must be a string."

    if not isinstance(size, list):
        return "'size' must be a list of lists."

    if not isinstance(properties, str):
        return "'properties' must be a string."

    ret = '\0'

    if filename.strip() == '':
        return 'Missing file name.'

    try:
        with h5py.File(filename, 'a') as f:
            ret = new_array(f, arrayname, size, properties)

    except IOError, e:
        logger.info(e)
        ret = "Can't open/create file '%s'." % (filename)
    except Exception, e:
        logger.info(e)
        return 'Internal error.'

    return ret
