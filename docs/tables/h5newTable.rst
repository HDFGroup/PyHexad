
.. _h5newTable:

Creating New Tables: ``h5newTable``
-----------------------------------

``h5newTable`` creates a new :term:`HDF5 table`. Table creation can be
customized via a creation property list.


.. rubric:: Excel UDF Syntax

::

  h5newTable(filename, tablename, heading)

  h5newTable(filename, tablename, heading [, properties])

 
.. rubric:: Mandatory Arguments

+-------------+---------------------------------------------------------------+
|Argument     |Description                                                    |
+=============+===============================================================+
|``filename`` |A text string specifying the name of an HDF5 file. If the file |
|             |doesn't exist, it will be created.                             |
+-------------+---------------------------------------------------------------+
|``tablename``|A text string (path) specifying the location of the HDF5 table.|
|             |Missing intermediate groups will be created automatically.     |
|             |Existing table will **not** be overwritten.                    | 
+-------------+---------------------------------------------------------------+
|``heading``  |A text string specifying the column names and types as a       |
|             |list of comma-separated ``Name,Type`` pairs. Comma characters  |
|             |in field names must be scaped by a backslash ``\`` character.  |
|             |Restrictions on the field types apply. See :ref:`types`.       |
+-------------+---------------------------------------------------------------+


.. rubric:: Optional Arguments

+---------------+-------------------------------------------------------------+
|Argument       |Description                                                  |
+===============+=============================================================+
|``properties`` |A text string that is formatted as a list of comma-separated |
|               |pairs of ``Name,Value`` arguments. See the **Properties**    |
|               |section for the supported keywords and value ranges.         |
|               |Unrecognized names (and their values) will be ignored.       |
+---------------+-------------------------------------------------------------+


.. rubric:: Properties

+--------------+---------------------------+--------------------+-------------+
|Name          |Description                |Values              |   Default   |
+==============+===========================+====================+=============+
|``Chunksize`` |Defines the chunk size for |A positive integer. |Auto.        |
|              |the table.                 |positive integers   |             |
+--------------+---------------------------+--------------------+-------------+   
|``Deflate``   |Enables GZIP compression   | (0-9)              |0 (no        |
|              |sets level.                |                    |compression) |
+--------------+---------------------------+--------------------+-------------+   
|``Fletcher32``|Enable Fletcher32 checksum |Boolean             |``false``    |
|              |generation for the array.  |                    |             |
+--------------+---------------------------+--------------------+-------------+   


.. rubric:: Return Value

On success, ``h5newTable`` returns ``tablename`` (string).

On error, an error message (string) is returned.


.. rubric:: Examples

Create a table with a single column of unsigned integers. Note that the
column name contains a comma character and needs to be escaped by ``\``.

::

   h5newTable("sample.h5", "/My/new/HDF5 table", "City\, State,uint8")


Create a table with 5 columns of different types.

::

   h5newTable("sample.h5", "/table2", \
              "City\, State,uint8,x,double,y,double,A\, B,int16,v,single[2]")


Create a table with four columns and control the chunk size (= 128 rows),
the compression level (= 6), and enable Fletche32 checksum generation.

::

   h5newTable("sample.h5", "/table3", \
              "Howdy,string,x,double,y,double,v,single[3]", \
              "Chunksize,128,Deflate,6,Fletcher32,true")


.. rubric:: Error Conditions
	    
The following conditions will create an error:

1. An invalid file name
   
   * An empty string or a string that contains characters not supported by
     the operating system
   * It refers to a file system location for which the user has insufficient
     access privileges.
   * It refers to a read-only file.
     
2. An invalid table name
   
   * An empty string
   * An HDF5 object exists at the specified location
   * Missing intermediate groups cannot be created.

3. An invalid heading

   * An empty string or a string which is not formatted as a comma-separated list
   * A (non-escaped) comma separated list with an odd number of elements
   * An invalid or unsupported datatype or fill value specification

4. Invalid properties

   * A string which is not formatted as a comma-separated list
   * A comma separated list with an odd number of elements
   * A value which is outside the admissible range for the corresponding key

.. rubric:: See Also
