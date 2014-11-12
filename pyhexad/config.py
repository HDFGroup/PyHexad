
from pyxll import xl_func


class Limits(object):

    EXCEL_MAX_ROWS = 1048576
    EXCEL_MAX_COLS = 16384


class Places(object):

    HDF5_HOME = 'C:\\Progra~1\\HDF_Group\\HDF5\\1.8.14'
    H52GIF = 'h52gifdll.exe'


#==============================================================================


@xl_func(": bool", volatile=True)
def h5py_is_installed():
    """returns True if h5py is installed"""
    try:
        import h5py
        return True
    except ImportError:
        return False

#==============================================================================


@xl_func(": string", volatile=True)
def h5py_version():
    """returns the h5py version"""
    try:
        import h5py
        return h5py.version.version
    except ImportError:
        return 'h5py is NOT installed.'

#==============================================================================


@xl_func(": string", volatile=True)
def numpy_version():
    """returns the numpy version"""
    try:
        import numpy
        return numpy.version.version
    except ImportError:
        return 'Numpy is NOT installed.'
