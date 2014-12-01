
Working with HDF5 Arrays
************************

HDF5 supports the storage of up to 32-dimensional arrays of an
arbitrary pre-defined or user-defined HDF5 element datatype.
This level of generality goes far beyond of what can be rendered on an
Excel worksheet and what might be of interest to most Excel users.
|product| supports standard tasks on one- and two-dimensional
HDF5 datasets of pre-defined scalar element types (integers, floating-point
numbers, strings). Standard array tasks include the reading of arrays
from an HDF5 file, the creation of new arrays in an HDF5 file, and the
writing of cell ranges to HDF5 arrays. This is the purpose of the three
|product| functions in the HDF5 array category:
:ref:`h5readArray <h5readArray>`, :ref:`h5newArray <h5newArray>`,
and :ref:`h5writeArray <h5writeArray>`. All three functions come with several
options, for example, to read or write only a sub-array, or to enable
compression of the HDF5 arrays in the file.


.. toctree::
   :maxdepth: 2

   h5readArray
   h5newArray
   h5writeArray
