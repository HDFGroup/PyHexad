Working with HDF5 Images
************************

An HDF5 file is a (smart) data container not just for numerical
data. It is well equipped to store other multi-media content, including
images, sounds, and video. Different communities have created several
standards describing domain-specific conventions for storing their
content in HDF5 files. The `HDF5 Image and Palette Specification
<http://www.hdfgroup.org/HDF5/doc/ADGuide/ImageSpec.html>`_ describes
how to store a large class of raster images in HDF5. |product| supports
the import and display of HDF5 images into a worksheet via the `h5readImage`
function.


.. toctree::
   :maxdepth: 2

   h5readImage
