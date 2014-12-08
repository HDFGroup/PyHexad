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

import tempfile
import os

THIS_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
TEST_FILES_DIRECTORY = os.path.join(
    THIS_DIRECTORY, os.pardir, os.pardir, 'testfiles'
)
TEMP_DIRECTORY = tempfile.gettempdir()
