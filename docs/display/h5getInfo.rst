
.. _h5getInfo:

``h5getInfo``
--------------

``h5showTree`` displays the contents of an HDF5 file in *hierarchical* or tree
view form. Starting at the HDF5 root group, all HDF5 objects in the HDF5 file
are visited recursively. Representations of HDF5 objects which are "deeper"
in the HDF5 hierarchy appear on a worksheet in cells farther to the right.
This mimics a tree-view within the confines of a worksheet.

Excel UDF Syntax
^^^^^^^^^^^^^^^^

::

  h5showTree(filename)

  h5showTree(filename, location)


Input Arguments
^^^^^^^^^^^^^^^
+----------+------------------------------------------------------------+
|Argument  |Description                                                 |
+==========+============================================================+
|`filename`|A text string specifying the name of an HDF5 file.          |
+----------+------------------------------------------------------------+
|`location`|A text string (path) specifying where to begin the traversal|
+----------+------------------------------------------------------------+

Return Value
^^^^^^^^^^^^
On success, ``h5showTree`` populates a range of cells with the requested
information.

On error, an error message (string) is returned.

Error Conditions
^^^^^^^^^^^^^^^^
The following conditions will create an error:

1. An invalid file name
   
  1. An empty string or a string that contains characters not supported by
     the operating system
  2. It refers to a file system location for which the user has insufficient
     access privileges
     
2. An invalid location
   
  1. An empty string
  2. No HDF5 object exists at the specified location

Examples
^^^^^^^^
Display detailed information about the HDF5 object a starting at location
``/HDFEOS/GRIDS`` in file ``file.he5``.

::
   
   h5showTree("file.he5", "/HDFEOS/GRIDS")


See Also
^^^^^^^^
[`h5getInfo`](https://github.com/HDFGroup/PyHexad/wiki/Reference-:-h5getInfo), [`h5showList`](https://github.com/HDFGroup/PyHexad/wiki/Reference-:-h5showList)

PyXLL Function
^^^^^^^^^^^^^^
