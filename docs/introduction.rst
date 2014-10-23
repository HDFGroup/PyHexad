
Introduction
============

The introduction goes here.

Installation
------------

To run PyHEXAD you need Excel, Python, NumPy, h5py, and PyXLL. (And you know how to install those...)

I have developed and tested PyHEXAD with the following configuration:

* Windows 8.1 Pro (64-bit)
* Excel 2013 (32-bit)
* Python 2.7.6.9 (32-bit)
* NumPy 1.8.1 (32-bit)
* h5py 2.3.1 (32-bit)
* PyXLL 2.2.1 (32-bit)

Other versions/combination will most likely work, but I have not tested them.

.. warning:: Don't try to mix architectures! It won't work. The components must all be either 32-bit or 64-bit. (Yes, there is a 64-bit version of PyXLL for the 64-bit version of Excel, but I haven't tried that.)

Update your ``pyxll.cfg`` file:

1. Make sure that the directory containing the ``pyhexad`` module is listed in the ``pythonpath`` section.

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



.. rubric:: Links

#. `Enthought <https://www.enthought.com/>`_
#. `The HDF Group <http://www.hdfgroup.org/>`_
#. `HDF5 <http://www.hdfgroup.org/HDF5/>`_
#. `h5py - HDF5 for Python <http://www.h5py.org/>`_
#. `PyXLL <https://www.pyxll.com/>`_
#. `Excel <http://office.microsoft.com/en-us/excel/>`_
#. `PyTables <http://www.pytables.org/moin>`_
#. `pandas <http://pandas.pydata.org/>`_
#. `MathWorks <http://www.mathworks.com/help/matlab/hdf5-files.html>`_
