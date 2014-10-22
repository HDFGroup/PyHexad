
import automation
import config
from config import Limits
import file_helpers
from file_helpers import file_exists
import functools
from functools import partial
import h5_helpers
from h5_helpers import path_is_valid_wrt_loc
import h5py
import logging
import numpy as np
import posixpath
import pyxll
from pyxll import xl_arg_doc, xl_func
import renderer
from renderer import draw

_log = logging.getLogger(__name__)

#===============================================================================

@xl_func("string filename, string location : string",
         category="HDF5",
         thread_safe=False,
         macro=True,
         disable_function_wizard_calc=True)
def h5getInfo(filename, location):
    """
    Display detailed information about a specific location in an HDF5 file.
        
    :param filename: the name of an HDF5 file
    :param location: an HDF5 path name (optional)
    :returns: A string
    """

#===============================================================================

    # sanity check
    
    if not isinstance(filename, str):
        raise TypeError, "'filename' must be a string."
    if not isinstance(location, str):
            raise TypeError, "'location' must be a string."
    if not file_exists(filename):
        return "Can't open file '%s' or the file is not an HDF5 file." %  \
            (filename)

    ret = '\0'

    with h5py.File(filename, 'r') as f:

        # normalize the HDF5 path

        path = location        
        if path != '':
            if not path in f:
                return 'Invalid location.'
        else:
            path = '/'

        # Is this a valid location?

        is_valid, species = path_is_valid_wrt_loc(f, path)
        if not is_valid:
            return 'Invalid location specified.'

        # generate the display - at the moment there are only two columns

        lines = []
        
        if species is None or isinstance(species, h5py.HardLink):
            # the location is loc is a file or group, or the path is a hardlink
        
            hnd = f
            if path != '/': hnd = f[path]

            num_attr = len(hnd.attrs)
            if num_attr > 0:
                lines.append(('Number of attributes:', num_attr))
                keys = hnd.attrs.keys()
                vals = hnd.attrs.values()
                for i in range(num_attr):
                    lines.append((keys[i], str(vals[i])))
            
            if isinstance(hnd, h5py.File) or isinstance(hnd, h5py.Group):

                num_links = len(hnd.keys())
                lines.append(('Number of links:', num_links))
                if num_links > 0:
                    lines.append(('Link names:', '\0'))
                    a = hnd.keys()
                    for i in range(num_links):
                        lines.append(('\0', a[i]))        

            elif isinstance(hnd, h5py.Dataset):

                lines.append(('Number of elements:', hnd.size))
                lines.append(('Shape:', str(hnd.shape)))
                lines.append(('Type:', str(hnd.dtype)))

            elif isinstance(hnd, h5py.Datatype):

                lines.append(('Type:', str(hnd.dtype)))

            else: # we should never get here
                raise Exception, 'What kind of hardlink is this???'

        elif isinstance(species, h5py.SoftLink) or \
             isinstance(species, h5py.ExternalLink):
            # we don't follow symlinks 4 now

            if isinstance(species, h5py.SoftLink):
                lines.append(('Link:', 'SoftLink'))
                lines.append(('Destination:', species.path))
            else: # external link
                lines.append(('Link:', 'ExternalLink'))
                lines.append(('Destination:', 'file://' + species.filename + \
                              '/' + species.path))

        else:
            # could be a user-defined link, which we ignore 4 now
            lines.append(('Link:', 'Unknown link type.'))
                
        # copy lines into Numpy array
        # Is that really necessary? No. Fix this!
            
        dty = h5py.special_dtype(vlen=str)
        a = np.empty((len(lines)+1, 2), dtype=dty)

        row = 0
        for l in lines:
            a[row] = l
            row += 1
            if row >= Limits.EXCEL_MAX_ROWS:
                break

        renderer.draw(a)

        return ret
