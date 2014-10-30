
import logging
import os
from tempfile import mktemp

import h5py
from pyxll import xl_func

from automation import xl_app
from config import Places
from file_helpers import file_exists
from h5_helpers import path_is_valid_wrt_loc

logger = logging.getLogger(__name__)

#===============================================================================


def get_image(loc, image_path, palette_path=None):
    """
    Returns the absolute path of a GIF image rendering of the
    HDF5 image at image_path
    """

    # Is this a valid location?
    is_valid, species = path_is_valid_wrt_loc(loc, image_path)
    if not is_valid:
        return (None, 'Invalid image path specified.')

    # Do we have datasets?
    if (loc.get(image_path) is None) or \
       (loc.get(image_path, getclass=True) != h5py.Dataset):
        return (None, "Can't open HDF5 image '%s'." % (image_path))

    if palette_path is not None:
        if (loc.get(palette_path) is None) or \
           (loc.get(palette_path, getclass=True) != h5py.Dataset):
            return (None, "Can't open HDF5 palette '%s'." % (palette_path))

    # try to run h52gif

    img = None

    try:

        exe = "%s\\bin\\%s" % (Places.HDF5_HOME, Places.H52GIF)
        gif = mktemp('.gif')
        cmd = '%s %s %s -i "%s"' % (exe, loc.file.filename, gif, image_path)
        if palette_path is not None:
            # There appears to be a bug in h52gif. The -p option is no longer
            # supported?
            #  cmd += ' -p "%s"' % (palette_path)
            pass

        os.system(cmd)
        img = gif

    except Exception, e:
        return (None, str(e))

    return (img, '\0')


#===============================================================================


@xl_func("string filename, string imagename, string palettename: string", category="HDF5")
def h5readImage(filename, imagename, palettename=None):
    """
    Reads an HDF5 image

    :param filename: the name of an HDF5 file
    :param imagename: the name of an HDF5 image
    :param palettename: the name of an HDF5 palette (optional)
    """

    ret = '\0'

    # sanity check

    if not isinstance(filename, str):
        return "'filename' must be a string."
    if not file_exists(filename):
        return "Can't open file '%s' or the file is not an HDF5 file." %  \
            (filename)

    if not isinstance(imagename, str):
        return "'imagename' must be a string."

    if palettename is not None:
        if not isinstance(palettename, str):
            return "'palettename' must be a string."

    try:
        with h5py.File(filename) as f:

            img, ret = get_image(f, imagename, palettename)

            if img is None:
                return ret
            if not os.path.exists(img):
                return 'Failed to create image file.'
            
            xl_app().ActiveSheet.Pictures().Insert(img)

    except Exception, e:
        logger.info(e)

    return ret
