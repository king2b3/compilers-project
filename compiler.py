""" Compiler structure, holds the error reporting.

    Parent to parser and scanner classes.

    Created on: 1-15-2021
    Version: Python 3.8.5
    Created by: Bayley King (https://github.com/king2b3)
"""
# line colors
from global_params import *
import sys

class Compiler():
    """ Base compiler class, holds the error message functions. """
    def __init__(self, filename, error_file='error_log.txt') -> None:
        self.filename = filename
        self.line_counter = 0
        self.error_status = None
        self.error_file = error_file

    def reportError(self, message) -> None:
        """ Prints error to terminal, and writes errors to log. """
        message = bcolors['FAIL'] + message + bcolors['ENDC']
        self.writeToErrorFile(message)
        sys.exit(message)
        self.error_status = True
    
    def reportWarning(self, message) -> None:
        """ Prints warnings to terminal, and writes warnings to log. """
        message = bcolors['WARNING'] + message + bcolors['ENDC']
        self.writeToErrorFile(message)
        print(message)

    def writeToErrorFile(self, message) -> None:
        """ Writes error messages to text file. """
        ef = open(self.error_file,'w')
        ef.write(message)
        ef.close()