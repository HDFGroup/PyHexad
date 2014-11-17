
.. _h5appendRows:

Appending Rows to a Table: ``h5appendRows``
-------------------------------------------

``h5appendRows`` appends rows to an existing HDF5 table.


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

.. note::
   The order of the columns in the row range must match the order of columns
   in the HDF5 table in the file.


.. rubric:: Return Value

On success, ``h5appendRows`` returns the number of rows appended.

On error, an error message (string) is returned.


.. rubric:: Examples

Append the rows in range `A1:C23581` on worksheet `Sheet2` to the HDF5 table
at `/Ask & Bid/20140423` in the file `tickdata.h5`.

::

   h5appendRows("tickdata.h5", "/Ask & Bid/20140423", Sheet2!$A1:C23581)
   
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
     
.. rubric:: See Also
