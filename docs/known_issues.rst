
Known Issues and Limitations
============================

.. warning::
   |product| has seen some basic testing, but it is not intended as a
   production solution. Use at your own risk!

Most |product| functions have a ``filename`` argument, for which
the path name of an HDF5 is expected. At the moment, providing an absolute
path name is the safest way to achieve the desired outcome.
For long path names, this is rather tedious. A simple workaround
might be to store a base path in a cell and then use a combination
of a cell reference and the Excel ``CONCATENATE`` function to construct
the full path name.

For relative path names, it is unclear what the default behavior should be.
They could be interpreted:

* Relative to an Excel default
* Relative to an environment variable
* Relative to the Excel workbook location (What about unsaved workbooks?)

Currently, the Excel default path ``C:\Users\<UserName>\Documents`` is
applied to relative file path names.

Please send your ideas and suggestions to the
`HDF forum <http://www.hdfgroup.org/services/support.html>`_!
