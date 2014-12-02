
What is |product|?
==================

|product| is an Excel add-in for accessing data stored in HDF5 files.
It provides about a dozen functions (see :ref:`fig-PyHexad`)
for reading and writing data,
and to create new HDF5 items from Excel. It aims to combine the ease of
use, and convenience of Excel with the performance and efficiency of
HDF5 smart data containers.

.. _fig-PyHexad:

.. figure:: ./PyHexad.png
   :align: center

   An Overview of PyHexad.


In its current form, the main audience might be intermediate Excel users
who like to spice up their workbooks with Excel functions and who might
have worked with external data sources such as relational databases.
These users will have a natural aversion against
"hardcoding", they understand what a refresh dependence is, and they have
some fluency in the symbology of referencing the content of cells on other
worksheets, etc. Of course, all |product| functions can be used with hand-coded
arguments, but many users will soon realize that automation is the real source
of productivity gains.

On the other end of the spectrum, for intermediate HDF5 users,
a "backstairs leading to an old ideal" is open again: For a lot of data
stored in HDF5 files, a spreadsheet software such as Excel is a very nice
user interface. Check it out!

`Wherever you are coming from, welcome to` |product|! Please help us improve
this product by sharing user stories, reporting issues, requesting new
features, and supporting the development.


Conventions
-----------

.. _conventions:

The syntax of the Excel functions provided by |product| is documented as
follows:

::

  h5function(A, B)

  h5function(A, B [, C, D, E])


Parameters in brackets, such as ``C``, ``D``, ``E`` in the previous example, are
**optional** parameters as opposed to mandatory parameters (``A`` and ``B``).

All parameters are **positional** parameters and must be used accordingly.
An example might help to illustrate their use. The call

::

  h5function(A, B, E)


passes ``E`` as the argument to the ``C`` position. This is quite different from

::

  h5function(A, B, , , E)


which passes ``E`` as argument in the ``E`` position. (and no arguments in the
``C`` and ``D`` positions)

Unfortunately, Excel functions have no *keyword* parameters and this is a
potential source of errors in using |product| functions.
