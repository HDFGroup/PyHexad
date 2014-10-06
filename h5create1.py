
import numpy as np
import h5py


supported_dtypes = {
    "DOUBLE":  np.double,
    "FLOAT32": np.single,
    "FLOAT64": np.double,
    "INT8":    np.int8,
    "INT16":   np.int16,
    "INT32":   np.int32,
    "INT64":   np.int64,
    "SINGLE":  np.single,
    "STRING":  h5py.special_dtype(vlen=str),
    "UINT8":   np.uint8,
    "UINT16":  np.uint16,
    "UINT32":  np.uint32,
    "UINT64":  np.uint64,
    }


def parse_heading(s):
    """
    When passed a correctly formatted header, this function returns a list with
    an even number of elements. Even entries contain column names and odd
    entries contain type decriptions. The latter must be verified separately.
    """
    
    slen = len(s)
    if slen == 0:
        raise Exception, 'Empty heading'

    lst = []
    
    low = 0
    high = 0
    while high < slen:
        high += 1

        if high == slen:
            if high == low:
                raise Exception, 'Empty value in heading found.'
            lst.append(s[low:high])
            break
        
        if s[high] == ',':
            if s[high-1] == '\\': # escaped delimiter
                continue
            else: # valid delimiter
                if high == low:
                    raise Exception, 'Empty value in heading found.'
                else:
                    lst.append(s[low:high])
                    low = high+1
        else:
            continue

    if len(lst) == 0 or not len(lst)%2 == 0:
        raise Exception, 'Invalid value count in heading.'

    # replace escaped commas in field names and do a sanity check
    # on the type values
    for i in range(0, len(lst), 2):
        lst[i] = lst[i].replace('\\,',',')
        if lst[i+1].count(':') > 1:
            raise Exception, 'Invalid type specification in heading'
            
    return lst


def dims_tuple_string(s):
    """
    Convert a string of dimensions 'DIM0 DIM1 ...' into a
    comma separated list 'DIM0, DIM1, ...' bearing in mind
    that Numpy wants (DIM0,) instead of (DIM0)
    """
    
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
    if not btype.upper() in supported_dtypes.keys():
        raise Exception, 'Unsupported type found.'
    else:
        if dims == None:
            return supported_dtypes[btype.upper()]
        else:
            return np.dtype(('(%s)%s' % (dims, t[0:alow])))


def dtype_from_heading(s):
    """
    Construct the Numpy dtype from a string description of the form
    Name1,Type1[:Fill1],...,NameN,TypeN[:FillN]
    Ther are certain restrictions on the set of types.
    """
    
    lst = parse_heading(str(s))

    check = set()
    descr = []
    
    for i in range(0, len(lst), 2):
        f = lst[i]
        check.add(f)
        t = lst[i+1]
        descr.append((f, parse_dtype(t)))

    if len(check) != len(lst)/2:
        raise Exception, 'Duplicate column name in heading found.'
        
    return np.dtype(descr)

    
with h5py.File('tables.h5','w') as h5:
    heading = 'No\, sir,uint8:123'
    dst = h5.create_dataset(heading, (0,),
                            dtype=dtype_from_heading(heading),
                            compression='gzip')

    heading = 'No\, sir,uint8:123,x,double,y,double,v,single[2]'
    dst1 = h5.create_dataset(heading, (0,),
                            dtype=dtype_from_heading(heading),
                            compression='gzip')

    heading = 'Howdy,uint8:123,x,double,y,double,v,single[3 3]'
    dst2 = h5.create_dataset(heading, (0,),
                            dtype=dtype_from_heading(heading),
                            compression='gzip')


    heading = 'Howdy,string,x,double,y,double,v,single[3]'
    dst2 = h5.create_dataset(heading, (0,),
                            dtype=dtype_from_heading(heading),
                            compression='gzip')
