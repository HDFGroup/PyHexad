"""
Creates a new HDF5 table, (extendible 1D dataset of an HDF5 compound datatype) and,
on success, returns a string (datasetname). A new HDF5 file be created, if it doesn't
exist already. Missing intermediate HDF5 groups will be generated automatically.
Existing datasets will NOT be overwritten and an error generated.
"""

import h5_helpers
from h5_helpers import path_is_available_for_obj
import h5py
import logging
import numpy as np
from pyxll import xl_arg_doc, xl_func
from table_helpers import dtype_from_heading

_log = logging.getLogger(__name__)

#===============================================================================

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_arg_doc("datasetname", "The name of the dataset to be created.")
@xl_arg_doc("heading", "The column names and types.")
@xl_arg_doc("plist", "An optional list of dataset creation properties.")
@xl_func("string filename, string datasetname, string heading, string plist : var",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=True)
def h5newTable(filename, datasetname, heading, plist=None):
    """
    Creates a new HDF5 table ("compound dataset").
    """
#===============================================================================

    if not isinstance(filename, str):
        return "'filename' must be a string."

    if not isinstance(datasetname, str):
        return "'datasetname' must be a string."

    if not isinstance(heading, str):
        return "'heading' must be a string."

    if plist != None:
        if not isinstance(plist, str):
            return "'plist' must be a string."

    ret = datasetname
    
    if filename.strip() == '':
        return 'Missing file name.'

    if datasetname.strip() == '':
        return 'Missing datasetname.'

    if heading.strip() == '':
        return 'Missing heading.'

    plist_ht = {}
    if plist.strip() != '':
        if len(plist.split(','))%2 != 0:
            return 'Invalid property list.'
        else: # convert the property list into a hashtable
            a = plist.split(',')
            for i in range(0,len(a),2):
                plist_ht[a[i].strip().upper()] = a[i+1].strip()

    try:
        with h5py.File(filename, 'a') as f:
            if not path_is_available_for_obj(f, datasetname, h5py.Dataset):
                return "Can't create dataset."

            # get type
            
            dty = None
            try:
                dty = dtype_from_heading(heading),
            except:
                return "Unsupported datatype specified."
           
            # parse property list

            kwargs = {}
            
            # chunking?
            if 'CHUNKSIZE' in plist_ht.keys():
                chunk = plist_ht['CHUNKSIZE']
                chunkdims = get_chunk_dimensions(chunk)
                if chunkdims == None:
                    return "Invalid chunk dimensions."
                if len(chunkdims) != len(dims):
                    return "Chunk rank must equal dataset rank (1)."
                kwargs['chunks'] = chunkdims

            if 'DEFLATE' in plist_ht.keys():
                lvl = plist_ht['DEFLATE']
                try:
                    lvl = int(lvl)
                    if lvl < 0 or lvl > 9:
                        return "Invalid compression level ([0-9])."
                    kwargs['compression'] = lvl
                except:
                    return "Invalid compression level ([0-9])."
            else:
                kwargs['compression'] = 4
                    
            # Fletcher32 check sum
            if 'FLETCHER32' in plist_ht.keys():
                bool = plist_ht['FLETCHER32']
                if bool.strip().lower() == 'true':
                    kwargs['fletcher32'] = True

            f.create_dataset(datasetname, (0,), dtype=dty[0], **kwargs)

    except IOError, e:
        _log.info(e)
        ret = "Can't open/create file."
    except Exception, e:
        _log.info(e)
        ret = 'Internal error.'
        
    return ret
