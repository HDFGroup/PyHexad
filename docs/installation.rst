
Installation
============

Generally, the installation is a two step process:

1. Verify that all the prerequisites are installed.
2. Install the |product| Python module.

At the moment, the entire process is automated only for
`Enthought Canopy <https://enthought.com/products/canopy/>`_.
If you are one of the lucky Canopy users you can skip the
remainder of this chapter after reading the next section.
For all other Python installations, please continue reading on
:ref:`sec-prerequisites` and the remainder of this chapter.

Install PyHexad from the Canopy Package Manager
-----------------------------------------------

.. todo: Didrik will populate this section.


.. _sec-prerequisites:

Prerequisites
-------------

|product| depends on Microsoft Excel, Python 2.x, NumPy, h5py, PyXLL, and HDF5.
Please download the prerequisites from the links provided below and follow
the respective installation instructions.

* `NumPy and h5py <http://www.lfd.uci.edu/~gohlke/pythonlibs/>`_
* `PyXLL <http://pyxll.com/download.html>`_
* `HDF5 <http://www.hdfgroup.org/HDF5/release/obtain5.html>`_

Our reference platform for |product| is configured as follows:

* Windows 8.1 Pro (64-bit)
* Excel 2013 (:strong:`32-bit`)
* Python 2.7.6.9 (:strong:`32-bit`)
* NumPy 1.8.2 (:strong:`32-bit`)
* h5py 2.3.1 (:strong:`32-bit`)
* PyXLL 2.2.1 (:strong:`32-bit`)
* HDF5 1.8.14 (64-bit)

Other versions/combination will most likely work, but I have not tested them.

.. warning::
   Don't try to mix architectures! It won't work. With the exception of the
   operating system and the HDF5 tools, all components must be either
   32-bit or 64-bit.

.. note::
   There are 64-bit versions of all components and there is a good chance
   that they'll just work, but this has **not** been tested.


The PyHexad Python Module
-------------------------

There are at least two other options for installing the PyHexad module.

.. rubric:: Use ``pip`` or ``setup.py`` and install PyHexad from PyPI

We have created a repository for PyHexad on `PyPI <https://pypi.python.org/pypi>`_.
If you have ``pip`` installed run::

  pip install pyhexad

Otherwise, download the package ``pyhexad-0.0.1.zip``, unpack it, and run::

  python setup.py install

.. rubric:: Use a Windows Installer

Download and run the Windows installer ``pyhexad-0.0.1.win32.exe`` and follow the
on-screen instructions.


Sanity Check
------------

After completing the installation, please verify that you have access
to the |product| functions from Excel. Here's a simple test:

1. Open a blank workbook in Excel.
2. Place the cursor into a cell of a workbook, type ``=h5py_version()``, and hit enter.

If the installation is "sane", while typing ``h5py_version``, AutoComplete will
already have suggested all kinds of completions starting with the ``h5`` prefix.
The result should be the version of your ``h5py`` installation displayed in the
cell where you placed that function call, e.g., ``2.3.1``.
