"""
BaseOutputFile class for generating output file name.
"""

class BaseOutputFile(object):

    def __init__(self):
        self._output_filename = None

    def output_filename(self):
        return self._output_filename
