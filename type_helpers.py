
import h5py
from h5py import special_dtype
import numpy as np

# supported scalar types

scalar_dtypes = {
    "BYTE":    np.int8,
    "DOUBLE":  np.double,
    "FLOAT":   np.single,
    "FLOAT32": np.single,
    "FLOAT64": np.double,
    "INT":     np.int32,
    "INT8":    np.int8,
    "INT16":   np.int16,
    "INT32":   np.int32,
    "INT64":   np.int64,
    "LONG":    np.int64,
    "SHORT":   np.int16,
    "SINGLE":  np.single,
    "STRING":  h5py.special_dtype(vlen=str),
    "UBYTE":   np.uint8,
    "UINT":    np.uint32,
    "UINT8":   np.uint8,
    "UINT16":  np.uint16,
    "UINT32":  np.uint32,
    "UINT64":  np.uint64,
    "ULONG":   np.uint64,
    "USHORT":  np.uint16
    }


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
