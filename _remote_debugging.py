"""
Debug-module enables remote debugging for Eclipse
=================================================

This module enables remote debugging for Eclipse.
http://pydev.org/manual_adv_remote_debugger.html

The Eclipse plug-in PyDev comes with a remote debugging file: pydevd
To identify where PyDev remote debugger Python files are, look in the
directory where you have Eclipse:
`C:\...\eclipse\plugins\org.python.pydev_x.y.z.xxxxxxxxxx\pysrc\`
Example:
'C:\Program Files\eclipse\plugins\org.python.pydev_2.7.5.2013052819\pysrc'
This path needs to be included in the Windows Pythonpath.
* Go to the Control Panel -> System -> Advanced -> Environment Variables.
* In the System variables panel, edit or add the variable "PYTHONPATH".
* Add the path to the variables value. Separating eventual previous paths with a semicolon.
* Restart applications that are dependent on the PYTHONPATH variable.

Usage:
------
When this module is placed in the MacrosSystem folder, it is loaded when Natlink starts.
To activate/deactivate the remote debugging, set the parameter
REMOTE_DEBUG to True or False, save the module then reload
via the "Messages from Python Macros"-window or restart DNS.
Once the script is loaded, you can set breakpoints in the Eclipse/PyDev IDE. 

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
