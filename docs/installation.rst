
Installation
============

Currently, the PyHexad installation is an manual process.
We are working to simplify and automate the installation process,
but decided against delaying this pre-release until a better
deployment experience became available.

The PyHexad installation is a two step process:

1. Install/verify the prerequisites.
2. Install the |product| Python module.

.. _sec-prerequisites:

Prerequisites
-------------

|product| depends on Microsoft Excel, Python 2.x, NumPy, h5py, PyXLL, and HDF5.
The recommended installation tool for installing Python packages is
`pip <https://pip.pypa.io/en/stable/installing.html>`_. Unfortunately, not all
packages support ``pip`` (yet). Please download the prerequisites from the
links provided below and follow the respective installation instructions.
Some of them come as Windows installers others as so-called ``wheel`` files,
for example, NumPy.
They can be installed by first installing the ``wheel`` module via
``pip install wheel`` and then running ``pip install some-package.whl``.

* `NumPy <http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy>`_ and `h5py <https://pypi.python.org/pypi/h5py/2.4.0>`_ 
* `PyXLL <http://pyxll.com/download.html>`_ (The 30 day trial version is sufficient for testing.) See `Installing the Excel Addin <https://www.pyxll.com/docs/index.html#installing-the-excel-addin>`_ for PyXLL installation instructions.
* [ `HDF5 <http://www.hdfgroup.org/HDF5/release/obtain5.html>`_ This is optional and only required, if you are interested in importing HDF5 images into Excel. See :ref:`sec-finishing-touches`. ]

.. warning::
   Don't try to mix architectures! It won't work. With the exception of the
   operating system and the HDF5 tools, all components must be either
   32-bit or 64-bit.

Our *reference platform* for |product| is configured as follows:

* Windows 8.1 Pro (64-bit)
* Excel 2013 (:strong:`32-bit`)
* ActivePython 2.7.6.9 (:strong:`32-bit`)
* NumPy 1.9.1 (:strong:`32-bit`)
* h5py 2.4.0 (:strong:`32-bit`)
* PyXLL 2.2.2 (:strong:`32-bit`)
* [ HDF5 1.8.14 (64-bit) ]

Other versions/combination will most likely work, but we have not tested them.

The ``pyhexad`` Python Module
-----------------------------

There are three options for installing the PyHexad module.

#. Use ``pip`` and install PyHexad from
   `PyPI <https://pypi.python.org/pypi/pyhexad>`_.
   Run ``pip install pyhexad``.
#. Download the package ``pyhexad-0.1.x.zip`` from
   `PyPI <https://pypi.python.org/pypi/pyhexad>`_, unpack it, and
   run ``python setup.py install``
#. Use the Windows Installer; download it from
   `PyPI <https://pypi.python.org/pypi/pyhexad>`_, run
   ``pyhexad-0.1.x.win32.exe`` and follow the on-screen instructions.

.. rubric:: Final Step: Tell PyXLL about ``pyhexad``

The PyXLL settings are controlled from a configuration file, ``pyxll.cfg``, in
the PyXLL installation directory, which is the directory where you unpacked
the PyXLL module. Your ``pyxll.cfg`` will be similar to the
following: ::

  [PYXLL]
  developer_mode = 1
  pythonpath =
      ./examples
  modules =
      misc
      worksheetfuncs
      customtypes
      asyncfunc
      menus
      automation
      callbacks
      objectcache
      tools.eclipse_debug
      tools.reload
  
  [LOG]
  verbosity = info
  format = %(asctime)s - %(levelname)s : %(message)s
  path = ./logs
  file = pyxll.%(date)s.log

Please add ``pyhexad`` to the ``modules`` section of the file. ::

  [PYXLL]
  developer_mode = 1
  pythonpath =
      ./examples
  modules =
      misc
      worksheetfuncs
      customtypes
      asyncfunc
      menus
      automation
      callbacks
      objectcache
      tools.eclipse_debug
      tools.reload
      pyhexad

  [LOG]
  verbosity = info
  format = %(asctime)s - %(levelname)s : %(message)s
  path = ./logs
  file = pyxll.%(date)s.log

That's it! With the heavy lifting out of the way, it's time to verify
that our effort wasn't in vain...


Sanity Check
------------

After completing the installation, please verify that you have access
to the |product| functions from Excel. Here's a simple test:

1. Open a blank workbook in Excel.
2. Place the cursor into a cell of a workbook, type ``=h5py_version()``,
   and hit enter.

If the installation is "sane", while typing ``h5py_version``, AutoComplete will
already have suggested all kinds of completions starting with the ``h5`` prefix.
The result should be the version of your ``h5py`` installation displayed in the
cell where you placed that function call, e.g., ``2.4.0``.

.. _sec-finishing-touches:


Finishing Touches
-----------------

In :ref:`sec-prerequisites`, we listed HDF5 1.8.14 as one of the dependencies.
There is only one function in PyHexad, ``h5readImage``, which currently depends
on the ``h52gif`` tool included in the standard Windows distribution of HDF5.
If you are not interested in reading HDF5 images into Excel, you are all set 
and ready for the next chapter (:ref:`chap-display`).

.. note::
   Good news: This dependence will most likely be gone in the release version,
   but it's there for now...

To ensure that PyHexad picks up a version of ``h52gif``, please
check that the configuration in PyHexad's ``config.py`` file matches
your local installation. ``config.py`` is located in your Python packages
directory, typically named ``site-packages``. For example, on my machine the
path is::

   C:\\Python27\\Lib\\site-packages\\pyhexad

``config.py`` stores the location and name of the ``h52gif`` tool in a class
called ``Places``::

  class Places(object):

      HDF5_HOME = 'C:\\Progra~1\\HDF_Group\\HDF5\\1.8.14'
      H52GIF = 'h52gifdll.exe'

If ``HDF5_HOME`` or ``H52GIF`` don't match your local installation, please
adjust them accordingly!
