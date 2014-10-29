
.. _h5readTable:

Reading Tables: ``h5readTable``
-------------------------------

``h5readTable`` reads rows from an :term:`HDF5 table`. There are variants for
reading a subset of columns or a contiguous or strided range of rows.


.. rubric:: Excel UDF Syntax

::

  h5readTable(filename, tablename)

  h5readTable(filename, tablename [, columns, first, last, step])

 
.. rubric:: Input Arguments

+-------------+-------------------------------------------------------------------+
|Argument     |Description                                                        |
+=============+===================================================================+
|``filename`` |A text string specifying the name of an HDF5 file                  |
+-------------+-------------------------------------------------------------------+
|``tablename``|A text string (path) specifying the location of an HDF5 table      |
+-------------+-------------------------------------------------------------------+
|``columns``  |An array of text strings specifying the columns to be read         |
+-------------+-------------------------------------------------------------------+
|``first``    |An integer specifying the first row to be read                     |
+-------------+-------------------------------------------------------------------+
|``last``     |An integer specifying the last row to be read                      |
+-------------+-------------------------------------------------------------------+
|``step``     |An integer specifying the number of rows to skip for each read row |
+-------------+-------------------------------------------------------------------+

.. rubric:: Return Value

On success, ``h5readTable`` populates a cell range with a the requested table
rows. The first row of the range contains the table heading (column names).

On error, an error message (string) is returned.


.. rubric:: Examples

Read the tick data for the CAD/CHF exchange rate from September 22, 2011.
	    
::

   h5readTable("cadchftickdata.h5", "/22-09-2011")

Sample the tickdata and read only every 10th value.
	    
::

   h5readTable("cadchftickdata.h5", "/22-09-2011", , , , 10)

Read the timestamp and ask only.
	    
::

   h5readTable("cadchftickdata.h5", "/22-09-2011", {"Time", "Ask"})

Read only ticks between rows 1,000 and 15,000.
	    
::

   h5readTable("cadchftickdata.h5", "/22-09-2011", , 1000, 15000)


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

3. The number of rows requested exceeds the maximum Excel row count 
     
4. An invalid column selection

   * An empty array
   * A column name that is not defined in the HDF5 table

5. An invalid first position

   * The is not empty and not a non-negative integer

6. An invalid last position

   * The argument is not empty and not a non-negative integer
       
7. An invalid step
   
   * The argument is not empty and not a positive integer

.. rubric:: See Also
