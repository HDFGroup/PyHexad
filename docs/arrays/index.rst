
Working with HDF5 Arrays
************************

HDF5 arrays are multi-dimensional arrays of a scalar element type
stored in an HDF5 file. (There's no such type restriction in HDF5 and
arrays of up to 32 dimensions are supported, but only one- or
two-dimensional arrays can be reasonably rendered on a worksheet.)

Standard array tasks include the reading of arrays from an HDF5 file,
the creation of new arrays in an HDF5 file, and the writing of
cell ranges to HDF5 arrays. This is the purpose of the three |product|
functions in the HDF5 array category: :ref:`h5readArray <h5readArray>`,
:ref:`h5newArray <h5newArray>`, and :ref:`h5writeArray <h5writeArray>`.
All three functions come with several options, for example, to read
or write only a sub-array, or to enable compression of the HDF5 arrays in
the file.


.. toctree::
   :maxdepth: 2

   h5readArray
   h5newArray
   h5writeArray
