""" Main file to call for the compilers project.

    Created on: 1-15-2021
    Version: Python 3.8.5
    Created by: Bayley King (https://github.com/king2b3)
"""

import argparse
import os
import re
from global_params import *
import sys
#from scanner import Scanner


def parse_arguments(
    args=None
) -> None:
    """ Returns the parsed arguments.

        Parameters
        ----------
        args: List of strings to be parsed by argparse.
          The default None results in argparse using the values passed into sys.args.
    """
    parser = argparse.ArgumentParser(
            description="A default template for python",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("input_file", help="Path to the input file.")
    parser.add_argument("-o", "--output_file", help="Path to the output file.",
            default="output")
    parser.add_argument("-p", "--print_all", help="Prints out EVERYTHING",
            default=False, action="store_true")
    parser.add_argument("-ps", "--print_scan", help="Prints out the scan",
            default=False, action="store_true")
    parser.add_argument("-pp", "--print_parse", help="Prints out the parsing",
            default=False, action="store_true")
    parser.add_argument("-n", "--name", help="Prints file name",
            default=False, action="store_true")
    parser.add_argument("-c", "--clear", help="clears the screen",
            default=False, action="store_true")
    args = parser.parse_args(args=args)
    return args

class Compiler():
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


def main(input_file, quiet=False, output_file="output", print_all=False, name=False,
                print_scan=False, print_parse=False, clear=False) -> None:
    """ Main function.

        Parameters
        ----------
        input_file: str:
          Path the input file.
        output_file: str
          Path to the output file. Default is 'output'
        quiet: bool
          Rather non-errors should be printed. Default is False
        print_parse: bool:
          Prints out the recursive calls of the parser. Default is False
        print_scan: bool:
          Prints out the scanned tokens. Default is False
        print_all: bool:
          Prints out everything. Default is False
        Returns
        -------
        int
          The exit code.
        Raises
        ------
        FileNotFoundError
          Means that the input file was not found.
    """
    #from timer import Timer
    from scanner import Scanner
    from parser import Parser
    from timer import Timer
    from os import system
    if clear: system("clear")

    compiler_timer = Timer()
    
    # Error check if the file even exists
    if not os.path.isfile(input_file):
        raise FileNotFoundError("File not found: {}".format(input_file))
    
    if name:
        print('#######################')
        print(input_file)
        print('#######################')
    compiler_timer.start_timer()
    p = Parser(input_file,print_bool=print_parse,sprint_bool=print_scan)
    p.parse()
    compiler_timer.end_timer()
    print(compiler_timer.__str__())

    return None


# Execute only if this file is being run as the entry file.
if __name__ == "__main__":
    import sys
    args = parse_arguments()
    try:
        main(**vars(args))
    except FileNotFoundError as exp:
        print(exp, file=sys.stderr)
        exit(-1)

