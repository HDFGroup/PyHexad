
.. _h5writeArray:

Writing Arrays: ``h5writeArray``
--------------------------------

``h5writeArray`` writes data from an Excel range to one- or two-dimensional
HDF5 arrays. There are variants for writing all elements, a contiguous
rectilinear subset (hyperslab), or a strided rectilinear subset of
an :term:`HDF5 array`.

If the HDF5 array does not already exist, it will be created and optional
arguments will be ignored.

Shape mismatches are handled within the extensibility limits of the destination
array. That is, an extensible array will be reshaped automatically to
accomodate the data within its specified bounds. For a fixed-shape array, a
shape mismatch will generate an error.


.. rubric:: Excel UDF Syntax

::

  h5writeArray(filename, arrayname, data)

  h5writeArray(filename, arrayname, data, [, first, last, step])

  
.. rubric:: Mandatory Arguments

+-------------+---------------------------------------------------------------+
|Argument     |Description                                                    |
+=============+===============================================================+
|``filename`` |A text string specifying the name of an HDF5 file              |
+-------------+---------------------------------------------------------------+
|``arrayname``|A text string (path) specifying the location of an HDF5 array  |
+-------------+---------------------------------------------------------------+
|``data``     |An Excel range of data to be written to the HDF5 array         |
+-------------+---------------------------------------------------------------+


.. rubric:: Optional Arguments

+---------+-------------------------------------------------------------------+
|Argument |Description                                                        |
+=========+===================================================================+
|``first``|An integer array specifying the position of the first element to   |
|         |be written                                                         |
+---------+-------------------------------------------------------------------+
|``last`` |An integer array specifying the position of the last element to be |
|         |written                                                            |
+---------+-------------------------------------------------------------------+
|``step`` |An integer array specifying the number of positions to skip in     |
|         |each dimension for each element written                            |
+---------+-------------------------------------------------------------------+

.. note:: The optional arguments are integer arrays whose length must be equal
	  to the rank (number of dimensions) of the HDF5 array.

   
.. rubric:: Return Value

On success, ``h5writeArray`` echos ``arrayname``.

On error, an error message (string) is returned.


.. rubric:: Examples

Write the content of cell range `$D3:I11` to HDF5 array at `/A/B/9 x 6`
in file `file.h5`. The array will be created if it doesn't exist already.

::

   h5writeArray("file.h5", "/A/B/9 x 6", $D3:I11)

Overwrite the fith row with values from range `$D24:I24`.

::

   h5writeArray("file.h5", "/A/B/9 x 6", $D24:I24, {5,1}, {5,6}, {1,1})


.. rubric:: Error Conditions
	    
The following conditions will create an error:

1. An invalid file name
   
   * An empty string or a string that contains characters not supported by
     the operating system
   * It refers to a file system location for which the user has insufficient
     access privileges
     
2. An invalid array name
   
   * An empty string
   * No HDF5 object exists at the specified location
   * The HDF5 object at the specified location is not an HDF5 array

3. An invalid data range

   * The cell content cannot be cast to a supported HDF5 array element type.
   
4. An invalid first position

   * The position is not empty and not an array of non-negative integers

5. An invalid last position

   * The position is not empty and not an array of non-negative integers
       
6. An invalid step

   * The position is not empty and not an array of positive integers


.. rubric:: See Also
:ref:`h5writeTable <h5writeTable>`, :ref:`h5writeAttribute <h5writeAttribute>`
