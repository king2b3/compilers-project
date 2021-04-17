""" Holds the symbol table structure for the language.
    
    SymbolTable holds two instances of the table object, one for global one for local
      Global is defined once and never changed, local is reset frequently
    
    Although this isn't the best representation, this grammar is simple enough to just allow
      a global and local symbol table.

    Created on: 3-29-2021
    Version: Python 3.8.5
    Created by: Bayley King (https://github.com/king2b3)
"""

from main import Compiler

class TypeCheck(Compiler):
    def __init__(self) -> None:
        ...
    
    def type_check(self, typ1:str, type2:str, case:int) -> int:
        """ Checks the type of two variables from the table.
        Returns enum error type to parser class
        """
        
        if case == 0:
            # int and floats can be mixed
            if type1 == "float" or type1 == "integer":
                if type2 != "float" and type2 != "int":
                    return 0
            else:
                return 1

        elif case == 1:
            # bool (> < == =) int is okay. 0 is false, else is true
            if type1 == "bool" or type1 == "integer":
                if type2 != "boolean" and type2 != "integer":
                    return 0
            else:
                return 1
        
        else:
            # normal case for assignment and comparison
            if type1 != type2:
                return 0
            else:
                return 1


