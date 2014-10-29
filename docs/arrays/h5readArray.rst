
.. _h5readArray:

Reading Arrays: ``h5readArray``
-------------------------------

``h5readArray`` reads elements of an HDF5 array. There are variants for
reading all elements, a contiguous rectilinear subset (hyperslab), or
a strided rectilinear subset of an HDF5 array.

.. rubric:: Excel UDF Syntax

::

  h5readArray(filename, arrayname)

  h5readArray(filename, arrayname, first, last)

  h5readArray(filename, arrayname, first, last, step)


.. todo:: *Everything below is out of date. Fix this!*
  
.. rubric:: Input Arguments

+------------+---------------------------------------------------------------+
|Argument    |Description                                                    |
+============+===============================================================+
|``filename``|A text string specifying the name of an HDF5 file              |
+------------+---------------------------------------------------------------+
|``location``|A text string (path) specifying the location of an HDF5 object |
+------------+---------------------------------------------------------------+
|``attr``    |A text string, the attribute's name                            |
+------------+---------------------------------------------------------------+

.. rubric:: Return Value

On success, ``h5readArray`` populates a cell with a string rendering of
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

   h5readArray("GSSTF.2b.2008.01.01.he5", \
                   "/HDFEOS/GRIDS/SET2/Data Fields/Tot_Precip_Water", \
		   "Units")

Read the ``HDFEOSVersion`` attribute of the object at ``/HDFEOS INFORMATION``.

::

   h5readArray(Sheet1!A1,"/HDFEOS INFORMATION", "HDFEOSVersion")
   		   
.. note:: The file name is retrieved from cell ``A1`` on the worksheet ``Sheet1``

.. rubric:: See Also
