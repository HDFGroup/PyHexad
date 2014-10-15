
import h5py

#===============================================================================

def is_object(filename, path):
    """
    Check if there is an object at 'path' in 'filename'.
    """
    if not (isinstance(filename, str) and isinstance(path, str)):
        raise TypeError, 'String expected.'
    
    ret = False
    try:
        with h5py.File(filename, 'r') as f:
            # is dataset or group
            cls = f.get(path, getclass=True)
            ret = (cls == h5py.Dataset) or (cls == h5py.Group)
    except Exception, e:
        pass
    return ret

#===============================================================================

def object_has_attribute(filename, path, attr):
    """
    Check if an HDF5 object has an HDF5 attribute with name 'attr'.
    """
    if not (isinstance(filename, str) and isinstance(path, str) and isinstance(attr, str)):
        raise TypeError, 'String expected.'

    ret = False
    try:
        with h5py.File(filename, 'r') as f:
            ret = attr in f[path].attrs
    except Exception, e:
        pass
    return ret

#===============================================================================

def path_is_available_for_obj(f, path, obj_type):
    """
    Check if a path is available for the creation of an object of a certain type.
    """

    if not (isinstance(f, h5py.File) or isinstance(f, h5py.Group)):
        raise TypeError, 'h5py file or group expected.'
    if not isinstance(path, str):
        raise TypeError, 'String expected.'
    if not ((obj_type == h5py.Group) or (obj_type == h5py.Dataset) or (obj_type == h5py.NamedDatatype)):
        raise TypeError, 'h5py object type expected.'
        
    if path == '' or path[-1] == '/': # the path is empty or has a trailing slash
        return False
    if path == '/' and obj_type == h5py.Group: # the root group
        return True
    if path == '/' and obj_type != h5py.Group: # can't have that
        return False

    is_absolute = False
    if path[0] == '/': # get rid of a leading slash (fake array element when split)
        is_absolute = True
        path = path[1:]
        
    a = path.split('/')
    ppath = '' # keep track of the current path
    if is_absolute:
        ppath = '/'

    for i in range(len(a)):
        ppath += a[i]
        if not ppath in f: # unused -> all set
            return True
        else: # path is in use
            if len(a) == 1 or i == len(a)-1: # this is the final leg
                cur_type = f.get(ppath,getclass=True)
                if cur_type != obj_type:
                    return False
                if obj_type == h5py.Group: # group exists
                    return True
                else: # the path is in use and not a group. can't overwrite.
                    return False
            else: # this is not the final leg -> must be group to continue
                if f.get(ppath, getclass=True) != h5py.Group:
                    return False
        ppath += '/'
        
#===============================================================================