
import logging
import tempfile

import h5py
from pyxll import xl_func

logger = logging.getLogger(__name__)

#==============================================================================


@xl_func("string filename: string",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=False)
def h5newFile(filename):
    """
    Creates a new HDF5 file. If no file name is specified a temporary file
    name will be generated at random.

    Existing files will not be overwritten.

    :param filename: the name of the HDF5 file to be created (optional)
    :returns: A string
    """

#==============================================================================

    if not isinstance(filename, str):
        raise TypeError("'filename' must be a string.")

    ret = '\0'

    if filename == '':
        filename = tempfile.mktemp('.h5')

    try:
        with h5py.File(filename, 'w-', libver='latest') as f:
            ret = filename

    except IOError, e:
        ret = "Can't create file '%s'." % (filename)
    except Exception, e:
        logger.info(e)
        return "Internal error."

    return ret
