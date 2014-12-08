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

#==============================================================================


def is_h5_location_handle(loc):
    """
    Returns if 'loc' is a valid location handle.
    Only HDF5 file or group handles are valid location handles.

    """
    return isinstance(loc, (h5py.File, h5py.Group))

#==============================================================================


def resolvable(loc, path):
    """
    Returns if (loc, path) can be resolved to an HDF5 object.
    """

    if not isinstance(path, str):
        raise TypeError("'path' must be a string.")

    if is_h5_location_handle(loc) and (path in loc):
        try:
            obj = loc.get(path, getclass=True)
            return True
        except KeyError:
            return False

#==============================================================================


def path_is_valid_wrt_loc(loc, path):
    """ Returns a tuple with the path_validity and the link type.

    Returns if 'path' is valid with respect to location 'loc'.
    The first return value (bool) indicates the validity.
    If the path is valid wrt. location, the second return value
    is the type of link or None, if the path is '/'.
    If the path is invalid wrt. location, the second argument is
    always none.

    """

    if is_h5_location_handle(loc) and isinstance(path, str) and (path in loc):
        if path != '/':
            try:

                # h5py throws an error when it encounters an unknown link type,
                # e.g., user-defined links

                link_type = loc.get(path, getlink=True)
                known_link_type = True

            except:  #FIXME: what kind of error is raised by h5py?

                known_link_type = False
                link_type = None
                pass

            return (known_link_type, link_type)
        else:
            # '/' is always valid with respect to a valid location
            return (True, None)
    else:
        return (False, None)

#==============================================================================


def path_is_available_for_obj(loc, path, obj_type):
    """
    Returns if a given path is available for the creation of a new HDF5 object
    of a certain class.

    Parameters
    ----------
    loc: h5py.File or h5py.Group
        An open file handle where to start.
    path: str
        the path for the new HDF5 object.
    obj_type: h5py.[Dataset, Dtatype, Group]

    """

    if not is_h5_location_handle(loc):
        return False
    if not isinstance(path, str):
        return False
    if not (obj_type in (h5py.Dataset, h5py.Datatype, h5py.Group)):
        return False

    if path == '' or path[-1] == '/':  # the path is empty or trailing slash
        return False
    if path == '/' and obj_type == h5py.Group:  # the root group
        return False
    if path == '/' and obj_type != h5py.Group:  # can't have that
        return False

    is_absolute = False
    if path[0] == '/':  # get rid of a leading slash (trouble when splitting)
        is_absolute = True
        path = path[1:]

    a = path.split('/')
    ppath = ''  # keep track of the current path
    if is_absolute:
        ppath = '/'

    # traverse the path segments and see what we've got

    for i in range(len(a)):
        ppath += a[i]

        if ppath not in loc:  # unused -> all set
            return True
        else:  # path is in use

            if len(a) == 1 or i == len(a)-1:  # this is the final leg

                if resolvable(loc, ppath):

                    cur_type = loc.get(ppath, getclass=True)
                    if cur_type != obj_type:
                        return False
                    if obj_type == h5py.Group:  # group exists
                        return True
                    else:  # path in use and not a group. can't overwrite.
                        return False

                else:  # cannot be resolved (dangling link)
                    return False

            else:  # this is not the final leg -> must be group to continue
                if resolvable(loc, ppath):
                    if loc.get(ppath, getclass=True) != h5py.Group:
                        return False
                else:  # cannot be resolved (dangling link)
                    return False

        ppath += '/'

#=============================================================================


def is_object(filename, path):
    """
    Check if there is an object at 'path' in 'filename'.
    """
    if not (isinstance(filename, str) and isinstance(path, str)):
        raise TypeError('String expected.')

    ret = False
    try:
        with h5py.File(filename, 'r') as f:
            # is dataset or group
            cls = f.get(path, getclass=True)
            ret = (cls == h5py.Dataset) or (cls == h5py.Group)
    except Exception:
        pass
    return ret

#==============================================================================


def object_has_attribute(filename, path, attr):
    """
    Check if an HDF5 object has an HDF5 attribute with name 'attr'.
    """
    if not (isinstance(filename, str) and isinstance(path, str) and
            isinstance(attr, str)):
        raise TypeError('String expected.')

    ret = False
    try:
        with h5py.File(filename, 'r') as f:
            ret = attr in f[path].attrs
    except Exception:
        pass
    return ret

#==============================================================================
