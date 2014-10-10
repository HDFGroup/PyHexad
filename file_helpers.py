
import h5py

def file_exists(filename):
    """
    Check if filename refers to an HDF5 file
    """

    if not isinstance(filename, str):
        raise TypeError, 'String expected.'
    
    result = False
    try:
        result = h5py.h5f.is_hdf5(filename)
    except Exception, e:
        pass
    return result
