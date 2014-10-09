
import pyxll
from pyxll import xl_arg_doc, xl_func
import h5py
import h5xl

import logging
_log = logging.getLogger(__name__)

#===============================================================================

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_arg_doc("groupname", "The name of the HDF5 group.")
@xl_func("string filename, string groupname: string",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=False)
def h5mkgroup(filename, groupname):
    """
    Creates an HDF5 group (and missing intermediate groups or the file)
    """

#===============================================================================

    if not isinstance(filename, str):
        raise TypeError, 'String expected.'

    if not isinstance(groupname, str):
        raise TypeError, 'String expected.'

    # WHAT COULD GO WRONG?
    #
    # 1. the file can't be created or opened
    # 2. the path name is in use and is not a group

    ret = groupname

    if filename.strip() == '':
        return 'Missing file name.'
    if groupname.strip() == '':
        return 'Missing group name.'

    try:
        with h5py.File(filename, 'a') as f:
            if h5xl.path_is_available_for_obj(f, groupname, h5py.Group):
                f.require_group(groupname)
                return groupname
            else:
                return "Can't create group."

    except IOError, e:
        _log.info(e)
        ret = "Can't open/create file."
    except Exception, e:
        _log.info(e)
        return "Internal error."
