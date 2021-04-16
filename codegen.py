""" C-based code generator structure

    Created on: 3-15-2021
    Version: Python 3.8.5
    Created by: Bayley King (https://github.com/king2b3)
"""

from datetime import datetime


class CodeGen():
    """ Structure to generate code from the parser
    """
    def __init__(self, filename) -> None:
        self.file_out_name = "temp_code_gen.c"
        # inits the files
        self.new_write_line("//Temp restricted C program generated from parser\n")
        # grabs the date and time of initial generation
        today = datetime.now()
        temp = "//File was generated at "
        temp += today.strftime("%Y/%m/%d %H:%M:%S")
        temp += "\n"
        self.write_line(temp)
        # Filename of compiled src program
        temp = "//Code gen of original file"
        temp += filename + "\n"
        self.write_line(temp)
        # include libraries
        self.write_line("#include <stdio.h>\n")
        
    def new_write_line(self, line):
        """ Creates the new file, or overwrites the old one """
        with open(self.file_out_name,'w') as fout:
            fout.write(line)
    
    def write_line(self, line):
        """ Appends a new line """
        with open(self.file_out_name,'a') as fout:
            fout.write(line)

    
def main():
    # tests the code gen file
    c = CodeGen('math.src')

if __name__ == "__main__":
    main()