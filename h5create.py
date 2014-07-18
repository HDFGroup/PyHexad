
from pyxll import xl_arg_doc, xl_func
import h5py
import h5xl
import numpy as np

import logging
_log = logging.getLogger(__name__)

supported_types = ('double', 'int64', 'int32', 'int16', 'int8',
                   'single', 'uint64', 'uint32', 'uint16', 'uint8')
#===============================================================================

def get_dimensions(size):
    # 'lst' is initialized by PyXLL as a list of lists, one list per row
    dims = []
    maxdims = []
    if len(size) == 1: # "row vector"
        num_col = len(size[0])
        if num_col == 0 or num_col > 32: # rank must be positive and not exceed 32
            return None
        for j in range(len(size[0])):
            if size[0][j] > 0:
                dims.append(size[0][j])
                maxdims.append(size[0][j])
            elif size[0][j] < 0:
                dims.append(-size[0][j])
                maxdims.append(None)
            else: # dimension must be non-zero
                return None
    else: # "colum vector"
        num_row = len(size)
        if num_row > 32: # rank must not exceed 32
            return None
        for i in range(len(size)):
            if len(size[i]) != 1: # row must have exactly one column
                return None
            if size[i][0] > 0:
                dims.append(size[i][0])
                maxdims.append(size[i][0])
            elif size[i][0] < 0:
                dims.append(-size[i][0])
                maxdims.append(None)
            else: # dimensions must be non-zero
                return None

    return dims, maxdims

#===============================================================================

def get_chunk_dimensions(chunk):
    """
    We expect a string of the form '[d1 d2 d3 ... dN]'
    """
    s = chunk.strip()
    if s[0] != '[' or s[-1] != ']':
        return None
    # strip the brackets
    s = s[1:-1]
    s1 = s.split()

    chunk = []
    for i in range(len(s1)):
        if s1[i].strip() != '':
            try:
                d = int(s1[i].strip())
                if d > 0:
                    chunk.append(d)  
                else: # can't have zero or negative entries
                    return None
            except:
                continue
                
    return tuple(chunk)

#===============================================================================

@xl_arg_doc("filename", "The name of an HDF5 file.")
@xl_arg_doc("datasetname", "The name of the dataset to be created.")
@xl_arg_doc("size", "The dimensions of the dataset to be created.")
@xl_arg_doc("plist", "An optional list of dataset creation properties.")
@xl_func("string filename, string datasetname, int[] size, string plist : string",
         category="HDF5",
         thread_safe=False,
         disable_function_wizard_calc=True)
def h5create(filename, datasetname, size, plist):
    """
    Creates a new dataset and, on success, returns a string (datasetname).
    A new HDF5 file be created, if it doesn't exist already.
    Missing intermediate HDF5 groups will be generated automatically.
    Existing datasets will NOT be overwritten and an error generated.

    Up to 32 dimensions are supported. Dimensions must be non-zero. A negative
    dimension is treated as unlimited and its absolute value will be used as
    the initial size.

    Dataset creation properties are specified as a list of name and value pair
    arguments: Name1,Value1,...,NameN,ValueN.

    Name: Datatype
    Purpose: Defines the datatype of the dataset.
    Values: [single, double, int8, int16, int32, int64, uint8, uint16, uint32, uint64]
    Default: double

    Name: ChunkSize
    Purpose: Defines the chunking layout of the dataset.
    Values: An array of positive integers of the same rank as the dataset
    Default: Not chunked.

    Name: Deflate
    Purpose: Enables GZIP compression.
    Values: [0-9]
    Default: 0 (no compression)

    Name: FillValue
    Purpose: Defines the fill value for numeric data sets.
    Values: Literal that can be converted to a value of the dataset element type.
    Default: 0

    Name: Fletcher32
    Purpose: Enable Fletcher32 checksum generation for the dataset.
    Values: Boolean
    Default: false

    Name: Shuffle
    Purpose: Enable the Shuffle filter.
    Values: Boolean
    Default: false
    """
#===============================================================================

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
    if not isinstance(size, list) or len(size) == 0:
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
            if not h5xl.path_is_available_for_obj(f, datasetname, h5py.Dataset):
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
                if not plist_ht['DATATYPE'] in supported_types:
                    return "Unsupported datatype specified."
                dty = np.dtype(plist_ht['DATATYPE'])
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
            # TODO: add a range check for integer fill values
            #
            if 'FILLVALUE' in plist_ht.keys():
                fv = plist_ht['FILLVALUE']
                try:
                    fv = float(fv)
                    if float(int(fv)) == fv:
                        fv = int(fv)
                    kwargs['fillvalue'] = fv
                except:
                    return "Invalid compression level ([0-9])."

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
