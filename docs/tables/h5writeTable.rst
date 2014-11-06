
.. _h5writeTable:

Writing to a Table: ``h5writeTable``
------------------------------------

``h5writeTable`` writes rows to an HDF5 table. Existing rows will
be overwritten, or the table extended as necessary. The write
operation can be restricted to a subset of columns.

.. caution::
   Unless the table is empty, this is generally not an append operation
   and will result in existing rows being overwritten. Use
   :ref:`h5appendRows` for appending rows to an HDF5 table.

.. rubric:: Excel UDF Syntax

::

  h5writeTable(filename, tablename, rows)

  h5writeTable(filename, tablename, rows [, columns])

  
.. rubric:: Mandatory Arguments

+-------------+---------------------------------------------------------------+
|Argument     |Description                                                    |
+=============+===============================================================+
|``filename`` |A text string specifying the name of an HDF5 file              |
+-------------+---------------------------------------------------------------+
|``tablename``|A text string (path) specifying the location of an HDF5 table  |
+-------------+---------------------------------------------------------------+
|``rows``     |An Excel range of rows to be written to the HDF5 table         |
+-------------+---------------------------------------------------------------+


.. rubric:: Optional Arguments

+-----------+-----------------------------------------------------------------+
|Argument   |Description                                                      |
+===========+=================================================================+
|``columns``|A string array listing the columns to be written.                |
+-----------+-----------------------------------------------------------------+


.. rubric:: Return Value

On success, ``h5writeTable`` returns the number of rows written.

On error, an error message (string) is returned.


.. rubric:: Examples

Read all elements of the ``Tot_Precip_Water`` array.

::

   h5writeTable("GSSTF.2b.2008.01.01.he5", \
               "/HDFEOS/GRIDS/SET2/Data Fields/Tot_Precip_Water")
   
Read only every other element of the ``Tot_Precip_Water`` array.

::

   h5writeTable("GSSTF.2b.2008.01.01.he5", \
               "/HDFEOS/GRIDS/SET2/Data Fields/Tot_Precip_Water", , , {2,2})

Read a contiguous rectangular region of the ``Tot_Precip_Water`` array.

::

   h5writeTable("GSSTF.2b.2008.01.01.he5", \
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
