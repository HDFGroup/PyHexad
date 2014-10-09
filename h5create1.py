
import numpy as np
import h5py
from table_helpers import dtype_from_heading

# run a few simple tests
    
with h5py.File('tables.h5','w') as h5:
    heading = 'City\, State,uint8:123'
    dst = h5.create_dataset(heading, (0,),
                            dtype=dtype_from_heading(heading),
                            compression='gzip')

    heading = 'City\, State,uint8:123,x,double,y,double,A\, B,int16,v,single[2]'
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
