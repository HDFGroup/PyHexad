
.. _h5newFile:

Creating Files: ``h5newFile``
-----------------------------

``h5newFiles`` creates a new HDF5 file. If no file name is provided,
a random file name will be generated and returned. Existing file will
not be overwritten and an error will be generated instead.


.. rubric:: Excel UDF Syntax

::

  h5newFile()

  h5newFile([filename])


.. rubric:: Optional Arguments

+-------------+---------------------------------------------------------------+
|Argument     |Description                                                    |
+=============+===============================================================+
|``filename`` |A text string specifying the name of an HDF5 file.             |
+-------------+---------------------------------------------------------------+


.. rubric:: Return Value

On success, ``h5newFile`` returns the file name of the newly created file.

On error, an error message (string) is returned.


.. rubric:: Examples

Create an HDF5 file at location ``c:\tmp\sample.h5``.

::

   h5newGroup("c:\tmp\sample.h5")
   

.. rubric:: Error Conditions
	    
The following conditions will create an error:

1. An invalid file name
   
   * An empty string or a string that contains characters not supported by
     the operating system
   * It refers to a file system location for which the user has insufficient
     access privileges.
   * A file exists at that location.
     
.. rubric:: See Also

:ref:`h5newGroup <h5newGroup>`
