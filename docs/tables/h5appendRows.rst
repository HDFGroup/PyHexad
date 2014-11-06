
.. _h5appendRows:

Writing to a Table: ``h5appendRows``
------------------------------------

``h5appendRows`` appends rows to an HDF5 table.


.. rubric:: Excel UDF Syntax

::

  h5appendRows(filename, tablename, rows)

.. rubric:: Mandatory Arguments

+-------------+---------------------------------------------------------------+
|Argument     |Description                                                    |
+=============+===============================================================+
|``filename`` |A text string specifying the name of an HDF5 file              |
+-------------+---------------------------------------------------------------+
|``tablename``|A text string (path) specifying the location of an HDF5 table  |
+-------------+---------------------------------------------------------------+
|``rows``     |An Excel range of rows to be appended to the HDF5 table        |
+-------------+---------------------------------------------------------------+


.. rubric:: Return Value

On success, ``h5appendRows`` returns the number of rows appended.

*Should this return the total number of rows in the table instead?*

On error, an error message (string) is returned.


.. rubric:: Examples

Read all elements of the ``Tot_Precip_Water`` array.

::

   h5appendRows("GSSTF.2b.2008.01.01.he5", \
               "/HDFEOS/GRIDS/SET2/Data Fields/Tot_Precip_Water")
   
Read only every other element of the ``Tot_Precip_Water`` array.

::

   h5appendRows("GSSTF.2b.2008.01.01.he5", \
               "/HDFEOS/GRIDS/SET2/Data Fields/Tot_Precip_Water", , , {2,2})

Read a contiguous rectangular region of the ``Tot_Precip_Water`` array.

::

   h5appendRows("GSSTF.2b.2008.01.01.he5", \
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
