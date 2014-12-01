
.. _h5readImage:

Reading Images: ``h5readImage``
-------------------------------

``h5readImage`` reads an :term:`HDF5 image` and renders it as Graphics
Interchange Format (GIF) image on an Excel worksheet.

.. rubric:: Excel UDF Syntax

::

  h5readImage(filename, imagename)

  h5readImage(filename, imagename [, palettename])


.. todo:: *What about hyperslabs?*
  
.. rubric:: Mandatory Arguments

+-------------+---------------------------------------------------------------+
|Argument     |Description                                                    |
+=============+===============================================================+
|``filename`` |A text string specifying the name of an HDF5 file              |
+-------------+---------------------------------------------------------------+
|``imagename``|A text string (path) specifying the location of an HDF5 image  |
+-------------+---------------------------------------------------------------+


.. rubric:: Optional Arguments

+---------------+-------------------------------------------------------------+
|Argument       |Description                                                  |
+===============+=============================================================+
|``palettename``|A text string (path) specifying the location of an HDF5      |
|               |palette                                                      |
+---------------+-------------------------------------------------------------+


.. rubric:: Return Value

On success, ``h5readImage`` renders a GIF image on an Excel worksheet.

On error, an error message (string) is returned.


.. rubric:: Examples

Read the ``hdflogo`` image.

::

   h5readImage("HDF5.h5", "/hdflogo")
   

.. rubric:: Error Conditions
	    
The following conditions will create an error:

1. An invalid file name
   
   * An empty string or a string that contains characters not supported by
     the operating system
   * It refers to a file system location for which the user has insufficient
     access privileges
     
2. An invalid image name
   
   * An empty string
   * No HDF5 object exists at the specified location
   * The HDF5 object at the specified location is not an HDF5 image

3. An invalid palette name
   
   * An empty string
   * No HDF5 object exists at the specified location
   * The HDF5 object at the specified location is not an HDF5 palette

.. rubric:: See Also

:ref:`h5readArray <h5readArray>`, :ref:`h5readAttribute <h5readAttribute>`,
:ref:`h5readTable <h5readTable>`

