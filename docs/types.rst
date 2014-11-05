
.. _types:

Supported Types
===============

Scalar Types
------------

Integers
^^^^^^^^


.. rubric:: Signed

+------------------+-------------+------------------------+
|Types             |Remarks      |HDF5 File Type          |
+==================+=============+========================+
| ``byte, int8``   | C ``char``  | ``H5T_STD_I8LE``       |
+------------------+-------------+------------------------+
| ``short, int16`` | C ``short`` | ``H5T_STD_I16LE``      |
+------------------+-------------+------------------------+
| ``int, int32``   | C ``int``   | ``H5T_STD_I32LE``      |
+------------------+-------------+------------------------+
| ``long, int64``  | C ``long``  | ``H5T_STD_I64LE``      |
+------------------+-------------+------------------------+


.. rubric:: Unsigned

+--------------------+----------------------+------------------------+
|Types               |Remarks               |HDF5 File Type          |
+====================+======================+========================+
| ``ubyte, uint8``   | C ``unsigned char``  | ``H5T_STD_U8LE``       |
+--------------------+----------------------+------------------------+
| ``ushort, uint16`` | C ``unsigned short`` | ``H5T_STD_U16LE``      |
+--------------------+----------------------+------------------------+
| ``uint, uint32``   | C ``unsigned int``   | ``H5T_STD_U32LE``      |
+--------------------+----------------------+------------------------+
| ``ulong, uint64``  | C ``unsigned long``  | ``H5T_STD_U64LE``      |
+--------------------+----------------------+------------------------+


Floating-Point Numbers
^^^^^^^^^^^^^^^^^^^^^^

+------------------------------+--------------+---------------------------+
|Types                         |Remarks       |HDF5 File Type             |
+==============================+==============+===========================+
| ``float, float32, single``   | C ``float``  | ``H5T_IEEE_F32LE``        |
+------------------------------+--------------+---------------------------+
| ``double, float64``          | C ``double`` | ``H5T_IEEE_F64LE``        |
+------------------------------+--------------+---------------------------+


Strings
^^^^^^^

+---------------+------------------------------------+------------------------+
|Types          |Remarks                             |HDF5 File Type          |
+===============+====================================+========================+
| ``stringN``   | Fixed-length C ASCII string of     |``H5T_C_S1``            |
|               | length ``N``                       |                        |
+---------------+------------------------------------+------------------------+
| ``string``    | Variable-length C ASCII string     |HDF5 varaiable-length   |
|               |                                    |ASCII string            |
+---------------+------------------------------------+------------------------+


Non-Scalar Types
----------------


Arrays
^^^^^^

An array type is specified as ``T[a b c ... n]`` where ``T`` is a scalar
type and ``a, b, c, ..., n`` are positive integers (dimensions). Array types
of up to 32 dimensions are supported.


Compounds
^^^^^^^^^

A compound type is specified as a comma separated list of field name and
type pairs ``Name1,Type1,Name2,Type2,...,NameN,TypeN`` where ``Name`` is an
ASCII string and ``Type`` is a scalar type name.

If ``Name`` contains a comma, it must be escaped with a backslash ``\``, e.g.,
``City\, State``.
