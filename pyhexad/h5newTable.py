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
from shape_helpers import get_chunk_dimensions
from table_helpers import dtype_from_heading

logger = logging.getLogger(__name__)

#==============================================================================


def new_table(loc, path, heading, plist=''):
    """
    Creates a new HDF5 table and returns a message (string)

    Parameters
    ----------
    loc: h5py.File or h5py.Group
        An open file handle where to start.
    path: str
        The path where to create the new table.
    heading: string
        The names and types of the table's columns.
    plist: string
        A list of dataset creation properties.
    """

    ret = path

    if not is_h5_location_handle(loc):
        raise TypeError('Location handle expected.')

    # check if the path is available
    if not path_is_available_for_obj(loc, path, h5py.Dataset):
        return "Can't create table at '%s'." % (path)

    plist_ht = {}
    if plist.strip() != '':
        if len(plist.split(',')) % 2 != 0:
            return 'Invalid property list.'
        # convert the property list into a hashtable
        a = plist.split(',')
        for i in range(0, len(a), 2):
            plist_ht[a[i].strip().upper()] = a[i+1].strip()

    try:

        # get type
        file_type = None

        try:
            file_type = dtype_from_heading(heading),
        except:
            return 'Unsupported datatype found.'

        # parse property list

        kwargs = {}

        # chunking?
        if 'CHUNKSIZE' in plist_ht.keys():
            try:
                chunk = "[%s]" % plist_ht['CHUNKSIZE']
                chunkdims = get_chunk_dimensions(chunk)
                if chunkdims is None:
                    return "Invalid chunk dimensions."
                if len(chunkdims) != 1:
                    return "Chunk rank must equal dataset rank (1)."
                kwargs['chunks'] = chunkdims
            except:
                return 'Invalid chunk size.'

        if 'DEFLATE' in plist_ht.keys():
            lvl = plist_ht['DEFLATE']
            try:
                lvl = int(lvl)
                if lvl < 0 or lvl > 9:
                    return "Compression level out of range [0-9]."
                kwargs['compression'] = lvl
            except:
                return "Invalid compression level ([0-9])."
        else:
            kwargs['compression'] = 4

        # Fletcher32 check sum
        if 'FLETCHER32' in plist_ht.keys():
            bool = plist_ht['FLETCHER32']
            if bool.strip().lower() == 'true':
                kwargs['fletcher32'] = True

        loc.create_dataset(path, (0,), maxshape=(None,), dtype=file_type[0],
                           **kwargs)

    except Exception, e:
        logger.info(e)
        ret = 'Internal error.'

    return ret

#==============================================================================


@xl_func("string filename, string tablename, string heading, string plist : string",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=True)
def h5newTable(filename, tablename, heading, properties):
    """
    Creates a new HDF5 table ("compound dataset").

    :param filename: the name of an HDF5 file
    :param tablename: the name of the HDF5 table to be created
    :param heading: the column names and types
    :param properties: a list of table creation properties (optional)
    :returns: A string
    """
#===============================================================================

    if not isinstance(filename, str):
        return "'filename' must be a string."

    if not isinstance(tablename, str):
        return "'tablename' must be a string."

    if not isinstance(heading, str):
        return "'heading' must be a string."

    if not isinstance(properties, str):
        return "'properties' must be a string."

    ret = '\0'

    if filename.strip() == '':
        return 'Missing file name.'

    try:
        with h5py.File(filename, 'a') as f:
            ret = new_table(f, tablename, heading, properties)

    except IOError, e:
        logger.info(e)
        ret = "Can't open/create file '%s'." % (filename)
    except Exception, e:
        logger.info(e)
        return 'Internal error.'

    return ret
