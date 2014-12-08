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

import setuptools
from distutils.core import setup

setup(
    name='pyhexad',
    version='0.1.0',
    author='The HDF Group, Enthought',
    author_email='gheber@hdfgroup.org, dpinte@enthought.com',
    url='http://www.hdfgroup.org/',
    description='An HDF5 Excel add-in using PyXLL',
    packages=setuptools.find_packages(),
)
