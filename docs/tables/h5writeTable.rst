
.. _h5writeTable:

Writing to a Table: ``h5writeTable``
------------------------------------

``h5writeTable`` writes rows to an existing HDF5 table. The write
operation can be restricted to a subset of columns.

.. caution::
   **This is a destructive operation.** Existing rows will be overwritten, or
   the table extended as necessary. Unless the table is empty, this is
   not an append operation. Use `h5appendRows` to append rows to an HDF5 table.


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

Overwrite the `Ask` column in the HDF5 table at `/Ask & Bid/20140423` in the
file `tickdata.h5` with data from the Excel range `B1:B23581` on worksheet
`Sheet2`.

::

   h5appendRows("tickdata.h5", "/Ask & Bid/20140423", Sheet2!$B1:B23581, "Ask")
   

.. rubric:: Error Conditions
	    
The following conditions will create an error:

1. An invalid file name
   
   * An empty string or a string that contains characters not supported by
     the operating system
   * It refers to a file system location for which the user has insufficient
     access privileges

2. An invalid table name
   
   * An empty string
   * No HDF5 object exists at the specified location
   * The HDF5 object at the specified location is not an HDF5 table

3. An invalid row set

   * The number or type of columns in the rows set does not match the
     number or type of columns in the file

4. An invalid set of columns.

   * One or more of the column names provided do not match the
     column names of the HDF5 table in the file.


.. rubric:: See Also
