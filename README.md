# Compilers Project for EECE 6083

## Development
This project uses Python 3.8.5, with no outside libraries. Any changes to this will be listed in this file.

---
## Usage
The project works off of arguments parsed through the command line. 

The following are all possible command line arguments
```
usage: main.py [-h] [-o OUTPUT_FILE] [-p] [-ps] [-pp] [-n] [-c] input_file

A default template for python

positional arguments:
  input_file            Path to the input file.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Path to the output file. (default: output)
  -p, --print_all       Prints out EVERYTHING (default: False)
  -ps, --print_scan     Prints out the scan (default: False)
  -pp, --print_parse    Prints out the parsing (default: False)
  -n, --name            Prints file name (default: False)
  -c, --clear           clears the screen (default: False)

```
---
## File Structure
main.py
- Controller program. 
- Contains the arg parsing.
- Inits the other files, passes parameters.
- Controls and runs the timer.
- Contains the Compiler class, which is parent for the other main classes.
  - Holds the error and warning reporting
  - Holds the file IO

scanner.py
- Front end scanner for the compiler. 
- Main use is to getToken() in parser.py

parser.py
- A top down LL1 parser, which calls and uses the scanner.
- Type checking and symbol table management is completed here.

symbol.py
- Contains the symbol table class. It is called in the other files

tokens.py
- List of reserved words
- Dictionary of token symbols
- Token Classes (ID, Keyword, Literal, Symbol, Null)

global_params.py
- Holds global variables
- Mostly used for the colored command line printing

fileTesting
- A bash script to call and run all the correct programs.
- Prints the file name, compile time along with any errors / warnings.
---
## Contact
Feel free to reach out to me here on GitHub if you are having any issues with my project.