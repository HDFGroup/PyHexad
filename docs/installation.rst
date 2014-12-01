
Installation
============

The installation is a two step process:

1. Verify that all the prerequisites are installed.
2. Install the |product| Python module.

At the moment, the first step is not automated and must be completed
by the user. Step number two work like any other Python module
installation.

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
   that they'll just work, but we have not tested them.

The PyHexad Python Module
-------------------------

There are three options for installing the PyHexad module.

.. rubric:: EasyInstall

If you have `EasyInstall <http://peak.telecommunity.com/DevCenter/EasyInstall>`_
run::

  easy_install -f https://enthought.com/pyhexad/package_index.html pyhexad


or, assuming you've downloaded the Python egg file,::

  easy_install ./pyhexad-0.0.1-py2.7.egg


.. rubric:: Windows Installer

Run the Windows installer ``pyhexad-0.0.1.win32.exe`` and follow the on-screen
instructions.

.. rubric:: Source Distribution

Unzip the source ``pyhexad-0.0.1.zip`` and run ``python setup.py`` in the unzipped
folder.

Sanity Check
------------

After completing the two previous steps, please verify that you have access
to the |product| functions from Excel. Here's a simple test:

1. Open a blank workbook in Excel.
2. Place the cursor into a cell of a workbook, type ``=h5py_version()``, and hit enter.

If the installation is "sane", while typing ``h5py_version``, AutoComplete will
already have suggested all kinds of completions. The result should be the version
of your ``h5py`` installation displayed in the cell where you placed that function
call, e.g., ``2.3.1``.
