
.. _h5newArray:

Creating New Arrays: ``h5newArray``
-----------------------------------

``h5newArray`` creates a new :term:`HDF5 array`. Array creation can be
customized via a creation property list.


.. rubric:: Excel UDF Syntax

::

  h5newArray(filename, arrayname, size)

  h5newArray(filename, arrayname, size [, properties])

 
.. rubric:: Mandatory Arguments

.. tabularcolumns::
   |p{0.2\textwidth}|p{0.7\textwidth}|

+-------------+---------------------------------------------------------------+
|Argument     |Description                                                    |
+=============+===============================================================+
|``filename`` |A text string specifying the name of an HDF5 file. If the file |
|             |doesn't exist, it will be created.                             |
+-------------+---------------------------------------------------------------+
|``arrayname``|A text string (path) specifying the location of the HDF5 array.|
|             |Missing intermediate groups will be created automatically.     |
|             |Existing arrays will not be overwritten.                       | 
+-------------+---------------------------------------------------------------+
|``size``     |An Excel array specifying the dimensions of the HDF5 array.    |
|             |Up to 32 dimensions are supported. Dimensions must be non-zero.|
|             |A negative dimension is treated as unlimited and its absolute  |
|             |value will be used as the initial size. ``size`` can be        |
|             |specified as a row or column cell range.                       |
+-------------+---------------------------------------------------------------+

.. caution::
   Although the creation of HDF5 arrays of more than two dimensions is
   supported, there is currently very little supporting functionality
   in |product| for accessing such HDF5 arrays.


.. rubric:: Optional Arguments

.. tabularcolumns::
   |p{0.2\textwidth}|p{0.7\textwidth}|
   
+---------------+-------------------------------------------------------------+
|Argument       |Description                                                  |
+===============+=============================================================+
|``properties`` |A text string that is formatted as a list of comma-separated |
|               |pairs of ``Name,Value`` arguments. See the **Properties**    |
|               |section for the supported keywords and value ranges.         |
|               |Unrecognized names (and their values) will be ignored.       |
+---------------+-------------------------------------------------------------+


.. rubric:: Properties

.. tabularcolumns::
   |p{0.15\textwidth}|p{0.3\textwidth}|p{0.3\textwidth}|p{0.15\textwidth}|
   
+--------------+---------------------------+--------------------+-------------+
|Name          |Description                |Values              |   Default   |
+==============+===========================+====================+=============+
|``Datatype``  |Defines the datatype of the|A scalar type.      | ``double``  |
|              |dataset.                   |See :ref:`types`.   |             |
+--------------+---------------------------+--------------------+-------------+
|``Chunksize`` |Defines the chunk size for |An array of         |Not chunked. |
|              |the dataset.               |positive integers   |             |
|              |                           |of the same rank    |             |
|              |                           |as the dataset.     |             |
+--------------+---------------------------+--------------------+-------------+   
|``Deflate``   |Enables GZIP compression   | (0-9)              |0 (no        |
|              |sets level.                |                    |compression) |
+--------------+---------------------------+--------------------+-------------+   
|``FillValue`` |Defines the fill value for |A literal that can  |0            |
|              |numeric array.             |converted to a value|             |
|              |                           |of the array element|             |
|              |                           |type.               |             |
+--------------+---------------------------+--------------------+-------------+   
|``Fletcher32``|Enable Fletcher32 checksum |Boolean             |``false``    |
|              |generation for the array.  |                    |             |
+--------------+---------------------------+--------------------+-------------+   
|``Shuffle``   |Enable the Shuffle filter. |Boolean             |``false``    |
+--------------+---------------------------+--------------------+-------------+   


.. rubric:: Return Value

On success, ``h5newArray`` returns ``arrayname`` (string).

On error, an error message (string) is returned.


.. rubric:: Examples

Create a two-dimensional 12x13 dataset of unsigned 1-byte integers with
contiguous layout:

::

   h5newArray("file.h5", "/A", {12, 13}, "Datatype,uint8")
   

Create a two-dimensional, extendible (in the second dimension) dataset of
single-precision floating-point numbers with chunked layout. The initial
extent of the dataset is 12x16 and a chunk size will be chosen automatically.

::

   h5newArray("file.h5", "/C/D", {12, -16}, "Datatype,single")


Create a three-dimensional, extendible (in the first dimension), gzip compressed
(level 6) dataset of double-precision floating-point numbers with chunked
(4x4x64 chunks) layout and Fletcher32 checksums generated.

::

   h5newArray("file.h5", "/E/F (gzipped + checksums)", {-12, 1024, 768}, \
              "ChunkSize,[4 4 64],Deflate,6,Fletcher32,true")


.. rubric:: Error Conditions
	    
The following conditions will create an error:

1. An invalid file name
   
   * An empty string or a string that contains characters not supported by
     the operating system
   * It refers to a file system location for which the user has insufficient
     access privileges.
   * It refers to a read-only file.
     
2. An invalid array name
   
   * An empty string
   * An HDF5 object exists at the specified location
   * Missing intermediate groups cannot be created.

3. An invalid array size

   * An empty array or an array which contains more than 32 elements
   * A zero dimension

4. Invalid properties

   * A string which is not formatted as a comma-separated list
   * A comma separated list with an odd number of elements
   * A value which is outside the admissible range for the corresponding key

.. rubric:: See Also

:ref:`h5newTable <h5newTable>`, :ref:`h5newGroup <h5newGroup>`
