
import h5py
from h5py import special_dtype
import numpy as np

# supported scalar types

scalar_dtypes = {
    "BYTE":    np.dtype(np.int8),
    "DOUBLE":  np.dtype(np.float64),
    "FLOAT":   np.dtype(np.float32),
    "FLOAT32": np.dtype(np.float32),
    "FLOAT64": np.dtype(np.float64),
    "INT":     np.dtype(np.int32),
    "INT8":    np.dtype(np.int8),
    "INT16":   np.dtype(np.int16),
    "INT32":   np.dtype(np.int32),
    "INT64":   np.dtype(np.int64),
    "LONG":    np.dtype(np.int64),
    "SHORT":   np.dtype(np.int16),
    "SINGLE":  np.dtype(np.float32),
    "STRING":  h5py.special_dtype(vlen=str),
    "UBYTE":   np.dtype(np.uint8),
    "UINT":    np.dtype(np.uint32),
    "UINT8":   np.dtype(np.uint8),
    "UINT16":  np.dtype(np.uint16),
    "UINT32":  np.dtype(np.uint32),
    "UINT64":  np.dtype(np.uint64),
    "ULONG":   np.dtype(np.uint64),
    "USHORT":  np.dtype(np.uint16)
    }

# Excel subsitution types

dtype_excel_substitute = {
    np.dtype(np.double):  np.dtype(np.float64),
    np.dtype(np.float32): np.dtype(np.float64),
    np.dtype(np.float64): np.dtype(np.float64),
    np.dtype(np.int8):    np.dtype(np.int32),
    np.dtype(np.int16):   np.dtype(np.int32),
    np.dtype(np.int32):   np.dtype(np.int32),
    np.dtype(np.int64):   np.dtype(np.int32),
    np.dtype(np.single):  np.dtype(np.float64),
    np.dtype(np.uint8):   np.dtype(np.int32),
    np.dtype(np.uint16):  np.dtype(np.int32),
    np.dtype(np.uint32):  np.dtype(np.int32),
    np.dtype(np.uint64):  np.dtype(np.int32)
    }

#===============================================================================

def is_supported_h5array_type(dty):

    if not isinstance(dty, np.dtype):
        raise TypeError, 'Numpy dtype expected.'
        
    return (dty in scalar_dtypes.values()) or (dty.kind == 'S')

#===============================================================================

def is_supported_h5table_type(dty):

    if not isinstance(dty, np.dtype):
        raise TypeError, 'Numpy dtype expected.'

    if dty.fields is None:
        return False

    for k in dty.fields:
        if not is_supported_h5array_type(dty.fields[k][0]):
            return False

    return True
    
#===============================================================================

def excel_dtype(dty):

    if not isinstance(dty, np.dtype):
        raise TypeError, 'Numpy dtype expected.'

    if dty.fields is None:
        if dty in dtype_excel_substitute.keys():
            return dtype_excel_substitute[dty]
        else:
            raise Exception, 'Unsupported scalar type.'
    else:
        spec = []
        for k in dty.fields:
            spec.append((k, excel_dtype(dty.fields[k][0])))
        return np.dtype(spec)
            
#===============================================================================

def dims_tuple_string(s):
    """
    Convert a string of dimensions 'DIM0 DIM1 ...' into a
    comma separated list 'DIM0, DIM1, ...' bearing in mind
    that Numpy wants (DIM0,) instead of (DIM0)
    """
    if not isinstance(s, str):
        raise TypeError, 'String expected.'

    dims = s.strip()
    a = dims.split(' ')
    rk = len(a)
    if rk == 0 or rk > 32:
        raise Exception, 'Invalid array rank found.'

    result = ''
    for i in range(0,rk):
        if int(a[i]) <= 0:
            raise Exception, 'Invalid array dimension found.'
        result = result + a[i]
        if i == 0:
            result = result + ','
    return result

#===============================================================================

def parse_dtype(s):
    """
    Given a string description, this function returns a corresponding
    Numpy dtype object. 
    """
    if not isinstance(s, str):
        raise TypeError, 'String expected.'

    t = s
    if s.find(':') > 0:
        t = s[0:s.find(':')] # for now, ignore the fill value

    # check if it is an array type
    alow = t.find('[')
    ahigh = t.find(']')
    dims = None
    if alow > 0: # potential array type
        if ahigh < 0:
            raise Exception, 'Incomplete array type?'
        # get the dimensions
        if alow > ahigh or alow == ahigh-1:
            raise Exception, 'Invalid array dimensions.'

        dims = dims_tuple_string(t[alow+1:ahigh])
    else: # not an array type
        alow = len(t)

    # lookup the base dtype
    btype = t[0:alow]
    if not btype.upper() in scalar_dtypes.keys():
        raise Exception, 'Unsupported scalar type found.'
    else:
        if dims == None:
            return scalar_dtypes[btype.upper()]
        else:
            return np.dtype(('(%s)%s' % (dims, t[0:alow])))