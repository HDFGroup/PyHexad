
.. _h5newGroup:

Creating Groups: ``h5newGroup``
-------------------------------

``h5newGroup`` creates a new HDF5 group.


.. rubric:: Excel UDF Syntax

::

  h5newGroup(filename, groupname)


.. rubric:: Mandatory Arguments

+-------------+---------------------------------------------------------------+
|Argument     |Description                                                    |
+=============+===============================================================+
|``filename`` |A text string specifying the name of an HDF5 file. If the file |
|             |doesn't exist, it will be created.                             |
+-------------+---------------------------------------------------------------+
|``groupname``|A text string (path) specifying the location of the HDF5 group.|
|             |Missing intermediate groups will be created automatically.     |
+-------------+---------------------------------------------------------------+


.. rubric:: Return Value

On success, ``h5newGroup`` returns ``groupname`` (string).

On error, an error message (string) is returned.


.. rubric:: Examples

Create an HDF5 group at location ``/My/new/HDF5 group``.

::

   h5newGroup("sample.h5", "/My/new/HDF5 group")
   

.. rubric:: Error Conditions
	    
The following conditions will create an error:

1. An invalid file name
   
   * An empty string or a string that contains characters not supported by
     the operating system
   * It refers to a file system location for which the user has insufficient
     access privileges.
   * It refers to a read-only file.
     
2. An invalid group name
   
   * An empty string
   * No HDF5 object that is not an HDF5 group exists at the specified location
   * Missing intermediate groups cannot be created.


.. rubric:: See Also

:ref:`h5newFile <h5newFile>`
