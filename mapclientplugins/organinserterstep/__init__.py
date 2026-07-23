
"""
MAP Client Plugin
"""

__version__ = '0.2.0'
__author__ = 'Elias Soltani'
__stepname__ = 'organinserter'
__location__ = 'https://github.com/mapclient-plugins/mapclientplugins.organinserterstep'

# import class that derives itself from the step mountpoint.
from mapclientplugins.organinserterstep import step

# Import the resource file when the module is loaded,
# this enables the framework to use the step icon.
from . import resources_rc
