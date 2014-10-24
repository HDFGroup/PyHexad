
import h5py
import numpy as np

#===============================================================================

def is_dims_array(a):
    """Determines if argument is a Numpy ndarray of integers"""

    if not isinstance(a, np.ndarray): return False
    if a.ndim != 1: return False
    if a.size > 32: return False
    if not np.issubdtype(a.dtype, np.int): return False
    if a.size == 0: return True

    return True

#===============================================================================

def is_non_zero_dims_array(a):
    """Determines if argument is a Numpy ndarray of non-zero integers"""

    if not is_dims_array(a): return False
    if np.count_non_zero(a) == len(a): return True

    return False

#===============================================================================

def is_non_negative_dims_array(a):
    """Determines if argument is a Numpy ndarray of non-negative integers"""

    if not is_dims_array(a): return False
    if np.amax(a) >= 0: return True

    return False

#===============================================================================

def is_positive_dims_array(a):
    """Determines if argument is a Numpy ndarray of positive integers"""

    if not is_dims_array(a): return False
    if np.amax(a) > 0: return True

    return False

#===============================================================================

def is_valid_hyperslab_spec(shape, first=None, last=None, step=None):
    """
    Determines if (first, last, step) describe a valid hyperslab selection
    on shape.

    CAUTION: we assume that shape is 0-based and that the hyperslab is 1-based
    """

    if not is_positive_dims_array(shape): return False
    
    rk = len(shape)
    if first is not None:
        if not is_non_negative_dims_array(first): return False
        if len(first) != rk: return False
    if last is not None:
        if not is_non_negative_dims_array(last): return False
        if len(last) != rk: return False
    if step is not None:
        if not is_non_negative_dims_array(step): return False
        if len(step) != rk: return False

    if first is not None and last is not None:
        if not np.greater_equal(last, first): return False

    if step is not None and last is not None:
        if np.greater_equal(step, last): return False
        
    return True

#===============================================================================

def get_dimensions(size):
    """
    'size' is a list of lists and we have to construct
    dims and maxdims lists from it
    """

    if not isinstance(size, list):
        raise TypeError, 'List expected.'

    dims = []
    maxdims = []
    if len(size) == 1: # "row vector"
        
        if not isinstance(size[0], list):
            raise TypeError, 'List expected.'
        
        num_col = len(size[0])
        if num_col == 0 or num_col > 32: # rank must be positive and not exceed 32
            return None
            
        for j in range(len(size[0])):

            if not isinstance(size[0][j], int):
                raise TypeError, 'Integer expected.'
            
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
            
            if not isinstance(size[i], list):
                raise TypeError, 'List expected.'
            if len(size[i]) != 1: # row must have exactly one column
                return None
            if not isinstance(size[i][0], int):
                raise TypeError, 'Integer expected.'            

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

    if not isinstance(chunk, str):
        raise TypeError, 'String expected.' 

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
