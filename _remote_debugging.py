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

To be able to import this module, you may also need to add the path to
the Natlink MacroSystem folder.
You may also have to add package files, i.e. empty-files with the name:
"__init__.py" to each folder containing your python files.

Usage:
------
This module is loaded globally. To activate/deactivate the remote debugging,
set the parameter REMOTE_DEBUG to True or False, save the module then reload
via the "Messages from Python Macros"-window or restart DNS.

Tip:
----
*Switch off debugging for normal use.*
While this debugging method works, I have experienced frequent crashes when
debugging is left on.
Leaving debugging on would potentially reduce performance and increase
response time.

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
        sys.stdout.write(">>> Pydevd remote debugging activated.\r\n")
    except ImportError:
        sys.stderr.write("Err: Failed to import Eclipse debug module, pydevd")
    except:
        sys.stderr.write("Eclipse debug server is not responding.")
