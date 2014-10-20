"""
Creates a new dataset and, on success, returns a string (datasetname).
A new HDF5 file be created, if it doesn't exist already.
Missing intermediate HDF5 groups will be generated automatically.
Existing datasets will NOT be overwritten and an error generated.
"""

import h5_helpers
from h5_helpers import path_is_available_for_obj
import h5py
import logging
import numpy as np
from pyxll import xl_arg_doc, xl_func
import shape_helpers
from shape_helpers import get_chunk_dimensions, get_dimensions
from type_helpers import parse_dtype

_log = logging.getLogger(__name__)

#===============================================================================

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_arg_doc("datasetname", "The name of the dataset to be created.")
@xl_arg_doc("size", "The dimensions of the dataset to be created.")
@xl_arg_doc("plist", "An optional list of dataset creation properties.")
@xl_func("string filename, string datasetname, int[] size, string plist : string",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=True)
def h5newArray(filename, datasetname, size, plist=None):
    """
    Creates a new multi-diensional HDF5 dataset of a scalar datatype.
    """
#===============================================================================

    if not isinstance(filename, str):
        return "'filename' must be a string."

    if not isinstance(datasetname, str):
        return "'datasetname' must be a string."

    if not isinstance(size, list):
        return "'size' must be a list of lists."

    if plist != None:
        if not isinstance(plist, str):
            return "'plist' must be a string."

    # WHAT COULD GO WRONG?
    #
    # 1. the file can't be created or opened
    # 2. the datasetname is in use
    # 3. the size specification is invalid (zero entries)
    # 4. the property list is invalid

    ret = datasetname
    
    if filename.strip() == '':
        return 'Missing file name.'

    if datasetname.strip() == '':
        return 'Missing datasetname.'

    if len(size) == 0:
        return 'Missing dataset size.'

    plist_ht = {}
    if plist.strip() != '' and len(plist.split(','))%2 != 0:
        return 'Invalid property list.'
    else: # convert the property list into a hashtable
        a = plist.split(',')
        for i in range(0,len(a),2):
            plist_ht[a[i].strip().upper()] = a[i+1].strip()

    try:
        with h5py.File(filename, 'a') as f:
            if not path_is_available_for_obj(f, datasetname, h5py.Dataset):
                return "Can't create dataset."

            kwargs = {}
                
            # get shape
            dims, maxdims = get_dimensions(size)
            if dims == None:
                return "Invalid dimensions specified."
            kwargs['shape'] = tuple(dims)
            kwargs['maxshape'] = tuple(maxdims)
                
            # parse property list                

            # get type
            dty = np.dtype('double')
            if 'DATATYPE' in plist_ht.keys():
                try:
                    dty = parse_dtype(plist_ht['DATATYPE'].upper())
                except:
                    return "Unsupported datatype specified."
            kwargs['dtype'] = dty

            # chunking?
            if 'CHUNKSIZE' in plist_ht.keys():
                chunk = plist_ht['CHUNKSIZE']
                chunkdims = get_chunk_dimensions(chunk)
                if chunkdims == None:
                    return "Invalid chunk dimensions."
                if len(chunkdims) != len(dims):
                    return "Chunk rank must equal dataset rank."
                kwargs['chunks'] = chunkdims

            # deflate?
            if 'DEFLATE' in plist_ht.keys():
                lvl = plist_ht['DEFLATE']
                try:
                    lvl = int(lvl)
                    if lvl < 0 or lvl > 9:
                        return "Invalid compression level ([0-9])."
                    kwargs['compression'] = lvl
                except:
                    return "Invalid compression level ([0-9])."

            # fill value
            #
            # TODO: implement fill-value & add a range check for integer fill values
            #
            #if 'FILLVALUE' in plist_ht.keys():
            #    fv = plist_ht['FILLVALUE']
            #    try:
            #        fv = float(fv)
            #        if float(int(fv)) == fv:
            #            fv = int(fv)
            #        kwargs['fillvalue'] = fv
            #    except:
            #        return "Invalid fill value."

            # Fletcher32 check sum
            if 'FLETCHER32' in plist_ht.keys():
                bool = plist_ht['FLETCHER32']
                if bool.strip().lower() == 'true':
                    kwargs['fletcher32'] = True

            # Shuffle
            if 'SHUFFLE' in plist_ht.keys():
                bool = plist_ht['SHUFFLE']
                if bool.strip().lower == 'true':
                    kwargs['shuffle'] = True

            # showtime!
            f.create_dataset(datasetname, **kwargs)
                   
    except IOError, e:
        _log.info(e)
        ret = "Can't open/create file."
    except Exception, e:
        _log.info(e)
        ret = 'Internal error.'
        
    return ret
