
import pyxll
from pyxll import xl_func
import h5py
import numpy
from numpy import dtype

import logging
_log = logging.getLogger(__name__)

# keywords for key/value pairs

_h5xl_keywords = {
    'CHUNKSIZE': None,
    'DATATYPE': ('DOUBLE', 'INT8', 'INT16', 'INT32', 'INT64',
                 'SINGLE', 'UINT8', 'UINT16', 'UINT32', 'UINT64'),
    'DEFLATE': (0,1,2,3,4,5,6,7,8,9),
    'FILLVALUE': None,
    'FLETCHER32': ('TRUE','FALSE','0','1','ON','OFF','ENABLE','DISABLE'),
    'MODE': ('MIN','SIMPLE'),
    'SHUFFLE': ('TRUE','FALSE','0','1','ON','OFF','ENABLE','DISABLE')
    }

supported_dtypes = (dtype('float32'), dtype('float64'),
                    dtype('int8'), dtype('int16'), dtype('int32'), dtype('int64'),
                    dtype('uint8'), dtype('uint16'), dtype('uint32'), dtype('uint64'))

#===============================================================================

def popup(title, message):
    import win32api, win32con
    win32api.MessageBox(0, str(message), str(title), win32con.MB_ICONWARNING)

#===============================================================================

def path_is_available_for_obj(f, path, obj_type):
    """
    Check if a path is available for the creation of an object of a certain type.
    """
    
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

def file_exists(filename):
    ret = False
    try:
        ret = h5py.h5f.is_hdf5(filename)
    except Exception, e:
        pass
    return ret

#===============================================================================

def get_tuple(dims):
    """
    Accept a list of lists and extract a dimension tuple
    """

    ret = []
    if len(dims) == 1: # "row vector"
        num_col = len(dims[0])
        if num_col == 0 or num_col > 32: # rank must be positive and not exceed 32
            return None
        for j in range(len(dims[0])):
            ret.append(dims[0][j])
    else: # "colum vector"
        num_row = len(dims)
        if num_row > 32: # rank must not exceed 32
            return None
        for i in range(len(size)):
            if len(dims[i]) != 1: # row must have exactly one column
                return None
            ret.append(dims[i][0])
            
    return ret
    
#===============================================================================

def is_supported_dataset(filename, path):
    ret = False
    try:
        with h5py.File(filename, 'r') as f:
            # is dataset
            ret = (f.get(path, getclass=True) == h5py.Dataset)
            # is one- or two-dimensional
            ret = (ret and (len(f[path].shape) == 1 or len(f[path].shape == 2)))
            # has the right type
            ret = (ret and (f[path].dtype in supported_dtypes))
    except Exception, e:
        pass
    return ret
    
#===============================================================================

def is_object(filename, path):
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
    ret = False
    try:
        with h5py.File(filename, 'r') as f:
            ret = attr in f[path].attrs
    except Exception, e:
        pass
    return ret

#===============================================================================

# return module version information

@xl_func(": string", volatile=True)
def hdf5_version():
    """returns the HDF5 version"""
    if not h5py_is_installed():
        return 'h5py is NOT installed.'

    try:
        import h5py
        return h5py.version.hdf5_version
    except ImportError:
        return 'HDF5 is NOT installed.'

#===============================================================================

@xl_func(": bool", volatile=True)
def h5py_is_installed():
    """returns True if h5py is installed"""
    try:
        import h5py
        return True
    except ImportError:
        return False

#===============================================================================

@xl_func(": string", volatile=True)
def h5py_version():
    """returns the h5py version"""
    try:
        import h5py
        return h5py.version.version
    except ImportError:
        return 'h5py is NOT installed.' 

#===============================================================================

@xl_func(": bool", volatile=True)
def numpy_is_installed():
    """returns True if numpy is installed"""
    try:
        import numpy
        return True
    except ImportError:
        return False

#===============================================================================

@xl_func(": string", volatile=True)
def numpy_version():
    """returns the numpy version"""
    try:
        import numpy
        return numpy.version.version
    except ImportError:
        return 'Numpy is NOT installed.'
