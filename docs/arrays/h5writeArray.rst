
.. _h5writeArray:

Writing Arrays: ``h5writeArray``
--------------------------------

``h5writeArray`` writes data to one- and two-dimensional HDF5 arrays.
There are variants for writing all elements, a contiguous rectilinear
subset (hyperslab), or a strided rectilinear subset of an :term:`HDF5 array`.


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
	  the rank (number of dimensions)
	  of the HDF5 array.

   
.. rubric:: Return Value

On success, ``h5writeArray`` echos ``arrayname``.

On error, an error message (string) is returned.


.. rubric:: Examples

Read all elements of the ``Tot_Precip_Water`` array.

::

   h5writeArray("GSSTF.2b.2008.01.01.he5", \
               "/HDFEOS/GRIDS/SET2/Data Fields/Tot_Precip_Water")
   
Read only every other element of the ``Tot_Precip_Water`` array.

::

   h5writeArray("GSSTF.2b.2008.01.01.he5", \
               "/HDFEOS/GRIDS/SET2/Data Fields/Tot_Precip_Water", , , {2,2})

Read a contiguous rectangular region of the ``Tot_Precip_Water`` array.

::

   h5writeArray("GSSTF.2b.2008.01.01.he5", \
               "/HDFEOS/GRIDS/SET2/Data Fields/Tot_Precip_Water", \
	       {25,10}, {356, 89})


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

3. The number of elements requested exceeds the maximum Excel row
   or column count
     
4. An invalid first position

   * The position is not empty and not an array of non-negative integers

5. An invalid last position

   * The position is not empty and not an array of non-negative integers
       
6. An invalid step

   * The position is not empty and not an array of positive integers


.. rubric:: See Also
