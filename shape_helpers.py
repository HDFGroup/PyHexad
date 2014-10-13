
import h5py
import numpy as np

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
