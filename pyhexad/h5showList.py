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

# We use H5Ovisit to traverse the hierarchy starting from a given location.
# We render the structure in tabular form where objects in an HDF5 group
# are listed under that group heading. The table is sparse, because most
# attributes apply only to certain object types.

from functools import partial
import logging
import posixpath

import h5py
import numpy as np
from pyxll import xl_func

from config import Limits
from file_helpers import file_exists
from h5_helpers import path_is_valid_wrt_loc
import renderer
from type_helpers import is_supported_h5array_type, is_supported_h5table_type, \
    dtype_to_hexad
from shape_helpers import tuple_to_excel

logger = logging.getLogger(__name__)

#==============================================================================


# the table heading layout, more columns to follow...

col_offset = (
    # (key, offset, display name)
    ('INDEX',    0, 'INDEX'),
    ('OBJ_TYPE', 1, 'OBJECT TYPE'),
    ('NAME',     2, 'OBJECT NAME'),
    ('#ATTR',    3, '#ATTRIBUTES'),
    ('#LNK',     4, '#LINKS'),
    ('DTYPE',    5, 'DATA TYPE'),
    ('RANK',     6, 'RANK'),
    ('DSPACE',   7, 'DATA SPACE'),
    ('DEST',     8, 'DESTINATION')
)

#==============================================================================


def render_row(grp, name):
    """
    render function for HDF5 objects
    """

    if not (isinstance(grp, (h5py.File, h5py.Group))):
        raise TypeError('HDF5 file or group expected.')

    if not isinstance(name, basestring):
        raise TypeError('String expected.')

    path = posixpath.join(grp.name, name)
    obj = grp[name]
    obj_type = grp.get(name, getclass=True)

    if obj_type == h5py.Group:

        return {
            'OBJ_TYPE': 'GROUP',
            'NAME': path,
            '#ATTR': len(obj.attrs.keys()),
            '#LNK': len(obj.keys())
        }

    elif obj_type == h5py.Dataset:

        # determine what kind of dataset
        flavor = 'DATASET'
        dty = obj.dtype
        if is_supported_h5array_type(dty):
            flavor = 'ARRAY'
        elif is_supported_h5table_type(dty):
            flavor = 'TABLE'

        return {
            'OBJ_TYPE': flavor,
            'NAME': name.split('/')[-1],
            '#ATTR': len(obj.attrs.keys()),
            'DTYPE': dtype_to_hexad(obj.dtype),
            'RANK': len(obj.shape),
            'DSPACE': tuple_to_excel(obj.shape)
        }

    elif obj_type == h5py.Datatype:

        return {
            'OBJ_TYPE': obj_type,
            'NAME': name.split('/')[-1],
            '#ATTR': len(obj.attrs.keys()),
            'DTYPE': dtype_to_hexad(obj.dtype),
        }

    else:
        return {
            'OBJ_TYPE': str(obj_type),
            'NAME': name.split('/')[-1],
        }

#==============================================================================


def render_table(loc, path):
    """
    Returns a list of sparse rows startting with the "table heading".
    """

    # check if the (loc, path) combo is valid
    is_valid, species = path_is_valid_wrt_loc(loc, path)

    if not is_valid:
        raise Exception('The specified path is invalid with respect to'
                        ' the location provided.')

    result = []

    # line for table heading
    ht = {}
    for c in col_offset:
        ht[c[0]] = c[2]
    result.append(ht)

    if species is None or isinstance(species, h5py.HardLink):
        # loc is file or group, or path is hardlink

        hnd = loc if path == '/' else loc[path]

        if isinstance(hnd, (h5py.File, h5py.Group)):

            # patch the name for the root group
            name = hnd.name.split('/')[-1]
            if name == '':
                name = '/'

            result.append(render_row(hnd.parent, name))

            #==================================================================
            # this is the callback for rendering links
            def print_obj(grp, name):
                result.append(render_row(grp, name))
            #
            #==================================================================

            hnd.visit(partial(print_obj, hnd))

        elif isinstance(hnd, (h5py.Dataset, h5py.Datatype)):

            result.append(render_row(hnd.parent, hnd.name.split('/')[-1]))

        else:  # we should never get here
            raise Exception('What kind of hardlink is this???')

    elif isinstance(species, (h5py.SoftLink, h5py.ExternalLink)):
        # we don't follow symlinks 4 now, just print the destination

        ht = {}
        ht['NAME'] = loc.name + '/' + path

        if isinstance(species, h5py.SoftLink):
            ht['OBJ_TYPE'] = 'SOFTLINK'
            ht['DEST'] = species.path
        else:
            ht['OBJ_TYPE'] = 'EXTERNALLINK'
            ht['DEST'] = 'file://' + species.filename + '/' + species.path

        result.append(ht)

    return result

#==============================================================================


@xl_func("string filename, string location : string",
         category="HDF5",
         thread_safe=False,
         macro=True,
         disable_function_wizard_calc=True)
def h5showList(filename, location):
    """
    Display contents of an HDF5 file in hierarchical form

    :param filename: the name of an HDF5 file
    :param location: an HDF5 path name (optional)
    :returns: A string
    """

    if not isinstance(filename, str):
        raise TypeError("'filename' must be a string.")
    if not isinstance(location, str):
            raise TypeError("'location' must be a string.")
    if not file_exists(filename):
        return "Can't open file '%s' or the file is not an HDF5 file." %  \
            (filename)

    ret = '\0'

    with h5py.File(filename, 'r') as f:

        ret = f.filename

        path = location
        if path != '':
            if path not in f:
                return 'Invalid location.'
        else:
            path = '/'

        is_valid, dummy = path_is_valid_wrt_loc(f, path)

        if not is_valid:
            return 'Invalid location specified.'

        # render the tree as a list of lines

        lines = render_table(f, path)

        if len(lines) >= Limits.EXCEL_MAX_ROWS:
            return 'The number objects in the file exceeds the maximum number' \
                'of rows of an Excel worksheet.'

        # generate the display in a Numpy array & patch in the INDEX column

        dty = h5py.special_dtype(vlen=str)
        a = np.empty((len(lines), len(col_offset)), dtype=dty)

        row = 0

        for i in range(0, len(lines)):
            a[row, 0] = row-1
            for k in col_offset:
                key = k[0]
                col = k[1]
                if key in lines[i].keys():
                    a[row, col] = lines[i][key]
            row += 1

        renderer.draw(a)

        return ret
