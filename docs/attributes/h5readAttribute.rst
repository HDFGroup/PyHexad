
.. _h5readAttribute:

Reading Attributes: ``h5readAttribute``
---------------------------------------

``h5readAttribute`` reads and renders the value of an HDF5 attribute.

.. rubric:: Excel UDF Syntax

::

  h5readAttribute(filename, location, attr)

.. rubric:: Input Arguments

+----------+---------------------------------------------------------------+
|Argument  |Description                                                    |
+==========+===============================================================+
|`filename`|A text string specifying the name of an HDF5 file              |
+----------+---------------------------------------------------------------+
|`location`|A text string (path) specifying the location of an HDF5 object |
+----------+---------------------------------------------------------------+
|`attr`    |A text string, the attrubte's name                             |
+----------+---------------------------------------------------------------+

.. rubric:: Return Value

On success, ``h5readAttribute`` populates a cell or range of cells with
the attribute value.

On error, an error message (string) is returned.

.. rubric:: Error Conditions
	    
The following conditions will create an error:

1. An invalid file name
   
   * An empty string or a string that contains characters not supported by
     the operating system
   * It refers to a file system location for which the user has insufficient
     access privileges
     
2. An invalid location
   
   * An empty string
   * No HDF5 object exists at the specified location

3. An invalid attribute name

   * An empty string
   * The HDF5 object doesn't have an attribute of that name

4. The attribute size exceeds XXX KB.
     
.. rubric:: Examples

Read the ``Units`` attribute of a dataset.

::
   
   h5readAttribute("GSSTF.2b.2008.01.01.he5",
                   "/HDFEOS/GRIDS/SET2/Data Fields/Tot_Precip_Water",
		   "Units")

.. rubric:: See Also
