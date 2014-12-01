
.. _h5writeAttribute:

Writing Attributes: ``h5writeAttribute``
----------------------------------------

``h5writeAttribute`` creates a new HDF5 attribute or updates
(**overwrites**!) the value of an existing one.


.. rubric:: Excel UDF Syntax

::

  h5writeAttribute(filename, location, attname, attvalue)


.. rubric:: Mandatory Arguments

+------------+---------------------------------------------------------------+
|Argument    |Description                                                    |
+============+===============================================================+
|``filename``|A text string specifying the name of an HDF5 file              |
+------------+---------------------------------------------------------------+
|``location``|A text string (path) specifying the location of an HDF5 object |
+------------+---------------------------------------------------------------+
|``attname`` |A text string, the HDF5 attribute's name                       |
+------------+---------------------------------------------------------------+
|``attvalue``|The attribute's value.                                         |
+------------+---------------------------------------------------------------+


.. rubric:: Return Value

On success, ``h5writeAttribute`` echoes the name of the HDF5 attribute written.

On error, an error message (string) is returned.


.. rubric:: Examples

Write the ``Units`` attribute of a dataset.

::

   h5writeAttribute("GSSTF.2b.2008.01.01.he5", \
                   "/HDFEOS/GRIDS/SET2/Data Fields/Tot_Precip_Water", \
		   "Units", "[mm]")

Write the ``HDFEOSVersion`` attribute of the object at ``/HDFEOS INFORMATION``.

::

   h5writeAttribute(Sheet1!A1,"/HDFEOS INFORMATION", "HDFEOSVersion", "5.1")


.. note:: In the last example, the file name is retrieved from cell ``A1``
	  on the worksheet ``Sheet1``


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


.. rubric:: See Also

:ref:`h5writeArray <h5writeArray>`, :ref:`h5writeTable <h5writeTable>`
