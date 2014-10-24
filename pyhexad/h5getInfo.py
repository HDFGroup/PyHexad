
from config import Limits
from file_helpers import file_exists
from h5_helpers import path_is_valid_wrt_loc
import h5py
import logging
import numpy as np
import renderer

logger = logging.getLogger(__name__)

#===============================================================================

def render_info(loc, path):
    """
    Returns a list of key/value pairs (more or less)


    Parameters
    ----------
    loc: an h5py file handler
        An open file handler where to search.
    path: str
        the path into the file that we are interested in.
    """

    # check if the (loc, path) combo is valid
    is_valid, species = path_is_valid_wrt_loc(loc, path)

    if not is_valid:
        raise ValueError(
            'The specified path is invalid with respect to the location provided.'
        )

    result = []

    if species is None or isinstance(species, h5py.HardLink):
        # the location is loc is a file or group, or the path is a hardlink
        
        hnd = loc
        if path != '/': hnd = loc[path]

        num_attr = len(hnd.attrs)
        if num_attr > 0:
            result.append(('Number of attributes:', num_attr))
            keys = hnd.attrs.keys()
            vals = hnd.attrs.values()
            for i in range(num_attr):
                result.append((keys[i], str(vals[i])))
            
        if isinstance(hnd, h5py.File) or isinstance(hnd, h5py.Group):

            num_links = len(hnd.keys())
            result.append(('Number of links:', num_links))
            if num_links > 0:
                result.append(('Link names:', '\0'))
                a = hnd.keys()
                for i in range(num_links):
                    result.append(('\0', a[i]))        

        elif isinstance(hnd, h5py.Dataset):

            result.append(('Number of elements:', hnd.size))
            result.append(('Shape:', str(hnd.shape)))
            result.append(('Type:', str(hnd.dtype)))

        elif isinstance(hnd, h5py.Datatype):

            result.append(('Type:', str(hnd.dtype)))

        else: # we should never get here
            raise Exception, 'What kind of hardlink is this???'

    elif isinstance(species, h5py.SoftLink) or \
         isinstance(species, h5py.ExternalLink):
        # we don't follow symlinks 4 now

        if isinstance(species, h5py.SoftLink):
            result.append(('Link:', 'SoftLink'))
            result.append(('Destination:', species.path))
        else: # external link
            result.append(('Link:', 'ExternalLink'))
            result.append(('Destination:', 'file://' + species.filename + \
                          '/' + species.path))

    else:
        # could be a user-defined link, which we ignore 4 now
        result.append(('Link:', 'Unknown link type.'))

    return result

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

        lines = render_info(f, path)

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
