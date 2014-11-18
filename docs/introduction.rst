
Introduction
============

The introduction goes here.

Installation
------------

To run |product| you need Excel, Python, NumPy, h5py, and PyXLL. (And you know
how to install those...)

We have developed and tested |product| with the following configuration:

* Windows 8.1 Pro (64-bit)
* Excel 2013 (32-bit)
* Python 2.7.6.9 (32-bit)
* NumPy 1.8.1 (32-bit)
* h5py 2.3.1 (32-bit)
* PyXLL 2.2.1 (32-bit)

Other versions/combination will most likely work, but I have not tested them.

.. warning:: Don't try to mix architectures! It won't work. The components must
	     all be either 32-bit or 64-bit. (Yes, there is a 64-bit version of
	     PyXLL for the 64-bit version of Excel, but we haven't tried that
	     yet.)

Update your ``pyxll.cfg`` file:

1. Make sure that the directory containing the ``pyhexad`` module is listed
   in the ``pythonpath`` section.

2. Add the ``pyhexad`` module to the ``modules`` section.

For example, the ``pyxll.cfg`` might look like this:

::

  [PYXLL]
  developer_mode = 1
  pythonpath =
	        ../../PyHexad

  modules =
        pyhexad

  [LOG]
  verbosity = info
  format = %(asctime)s - %(levelname)s : %(message)s
  path = ./logs
  file = pyxll.%(date)s.log



  
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
