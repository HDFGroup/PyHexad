
import file_helpers
from file_helpers import file_exists
import h5_helpers
from h5_helpers import path_is_valid_wrt_loc
import h5py
import pyxll
from pyxll import xl_func

#===============================================================================

@xl_func("string filename, string location, string attr: string",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=True)
def h5readAttribute(filename, location, attr):
    """
    Reads and returns a string repesentation of the value of an HDF5 attribute.
    
    :param filename: the name of an HDF5 file
    :param location: the location of a HDF5 object 
    :param attr:     the name of an HDF5 attribute
    :returns: A string
    """

    if not isinstance(filename, str):
        raise TypeError, 'String expected.'
    if not isinstance(location, str):
        raise TypeError, 'String expected.'
    if not isinstance(attr, str):
        raise TypeError, 'String expected.'
    if not file_exists(filename):
        return "Can't open file '%s' or the file is not an HDF5 file." %  \
            (filename)

    with h5py.File(filename, 'r') as f:

        path = location        
        if path != '':
            if not path in f:
                return "Invalid location '%s'." % (path)
        else:
            path = '/'

        is_valid, species = path_is_valid_wrt_loc(f, path)

        if not is_valid:
            return 'Invalid location specified.'

        # Is there an object at location and does it have that attribute? 

        obj = f.get(path)
        if obj is not None:
            if attr in obj.attrs:
                return str(obj.attrs[attr])
            else:
                return "No attribute named '%s' found." % attr
        else:
            return "No object at location '%s'." % location
