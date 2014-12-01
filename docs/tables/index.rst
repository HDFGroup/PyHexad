
Working with HDF5 Tables
************************

HDF5 tables are one-dimensional, extensible HDF5 datasets whose elements
are of an HDF5 compound datatype. |product| supports compound types whose
fields ("columns") are scalar, pre-defined HDF5 datatypes
(integers, floating-point numbers, strings). There are currently four
Excel functions in |product| to support standard oerpations on HDF5 tables.

The first function, `h5readTable`, can be used to read an entire HDF5 table
into Excel or just a subset of columns or rows.

The second function, `h5newTable`, lets one create a new HDF5 table
and customize its properties.

The third and fourth functions, `h5appendRows` and `h5writeTable`, allow
one to append rows to an existing HDF5 table or overwrite existing rows.

.. caution::
   Beyond the name `table`, HDF5 tables don't share very much with their
   relational cousins. At the file level, they are stored as HDF5 datasets
   and that largely dictates their "semantics", which means that reading
   from and writing to an HDF5 table is much more akin to accessing
   an array than querying or updating a relational table. See [PyTables]_
   and [pandas]_ for better table abstractions on top of HDF5.

.. toctree::
   :maxdepth: 2

   h5readTable
   h5newTable
   h5appendRows
   h5writeTable
