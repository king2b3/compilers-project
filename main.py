'''
    main file for compilers class project
    Bayley King
    Python 3
'''

import argparse
import os
import re
#from scanner import Scanner


def parse_arguments(
    args=None
) -> None:
    """Returns the parsed arguments.

    Parameters
    ----------
    args: List of strings to be parsed by argparse.
        The default None results in argparse using the values passed into
        sys.args.
    """
    parser = argparse.ArgumentParser(
            description="A default template for python",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("input_file", help="Path to the input file.")
    parser.add_argument("-o", "--output_file", help="Path to the output file.",
            default="output")
    parser.add_argument("-q", "--quiet", help="Don't print out non-errors",
            default=False, action="store_true")
    args = parser.parse_args(args=args)
    return args


class Compiler():
    def __init__(
        self, filename,
        error_file='error_log.txt'
    ):
        self.filename = filename
        self.line_counter = 0
        self.error_status = None
        self.error_file = error_file

        
        #self.s = Scanner()


    def reportError(
        self, message
    ) -> None:
        ''' Prints error to terminal, and writes errors to log
        '''
        message =+ 'on line ' + self.line_counter
        self.writeToErrorFile(message)
        print(message)
        self.error_status = True
    
    def reportWarning(
        self, message
    ) -> None:
        ''' Prints warnings to terminal, and writes warnings to log
        '''
        message =+ 'on line ' + self.line_counter
        self.writeToErrorFile(message)
        print(message)


    def writeToErrorFile(
        self, message
    ) -> None:
        ''' Writes error messages to text file
        '''
        ef = open(self.error_file,'w')
        ef.write(message)
        ef.close()


def main(
    input_file, 
    quiet=False, output_file="output"
) -> None:
    """Main function.

    Parameters
    ----------
    input_file: str:
        Path the input file.
    output_file: str
        Path to the output file. Default is 'output'
    quiet: bool
        Rather non-errors should be printed. Default is False
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

    #compiler_timer = Timer()
    
    # Error check if the file even exists
    if not os.path.isfile(input_file):
        raise FileNotFoundError("File not found: {}".format(input_file))
    
    c = Compiler(input_file)
    s = Scanner(input_file)

    token = s.getToken()
    while token != '.':
        print(token)
        token = s.getToken()
        c.error_status = s.error_status
        c.line_counter = s.line_counter

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

