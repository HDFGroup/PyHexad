##############################################################################
# Copyright by The HDF Group.                                                #
# All rights reserved.                                                       #
#                                                                            #
# This file is part of PyHexad. The full PyHexad copyright notice, including #
# terms governing use, modification, and redistribution, is contained in     #
# the file COPYING, which can be found at the root of the source code        #
# distribution tree.  If you do not have access to this file, you may        #
# request a copy from help@hdfgroup.org.                                     #
##############################################################################

from setuptools import setup, find_packages

setup(
    name='pyhexad',
    version='0.1.2',
    author='The HDF Group, Enthought',
    author_email='gheber@hdfgroup.org, dpinte@enthought.com',
    url='http://www.hdfgroup.org/',
    description='An HDF5 Excel add-in using PyXLL',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='excel hdf5 pyxll',
    packages=find_packages(),
    entry_points = {
        'pyxll.extensions': [
            'pyhexad = pyhexad.pyxll_extension:load'
        ]
    }
)
