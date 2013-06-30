#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Debug-module enables remote debugging for Eclipse
=================================================

This module enables remote debugging for Eclipse. This means debugging an
external process, even over a network connection.

The Eclipse plug-in PyDev comes with a remote debugging file: pydevd
To identify where PyDev remote debugger Python files are, look in the
directory where you have Eclipse:
`C:\...\eclipse\plugins\org.python.pydev_x.y.z.xxxxxxxxxx\pysrc\`
Example:
'C:\Program Files\eclipse\plugins\org.python.pydev_2.7.5.2013052819\pysrc'
This path needs to be included in the Python path.


Usage:
------
Simply import this module in your scripts, and to set breakpoints, i hope.

"""

import sys

REMOTE_DEBUG = True  # Switch remote debugging on or off
ADDRESS = 'localhost'  # 'localhost' or IP number, ex: '10.0.0.3'
PORT = 5678  # Eclipse standard debug server port.

# ------------------------------------------------------------

if REMOTE_DEBUG:
    try:
        import pydevd
        pydevd.settrace(ADDRESS, port=PORT, suspend=False,
            # Redirect stdout and stderr to eclipse console
            stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Err: Failed to import Eclipse debug module, pydevd")
    except:
        sys.stderr.write("Eclipse debug server is not responding.")
