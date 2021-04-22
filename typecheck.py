""" Holds the type checking framework.

    Methods return 0 or 1 if the type check is successful or not

    Created on: 3-29-2021
    Version: Python 3.8.5
    Created by: Bayley King (https://github.com/king2b3)
"""

from tokens import *

class TypeCheck():
    
    def type_check(self, type1:str, type2:str) -> int:
        """ Checks the type of two variables from the table.
            Returns enum error type to parser class
        """

        # int and floats can be mixed
        if (type1 == "float" or type1 == "integer") and (type2 != "float" and type2 != "integer"):
            return 0

        # bool (> < == =) int is okay. 0 is false, else is true
        elif (type1 == "bool" or type1 == "integer") and (type2 != "bool" and type2 != "integer"):
            return 0
    
        # normal case for assignment and comparison
        elif type1 != type2:
            return 0
        
        # passes type checking
        else:
            return 1

    def hard_check(self, type1:str, type2:str) -> int:
        """ Checks for procedure returns, and other explicit cases """
        return type1 == type2
    
    def array_check(self, type1:str, type2:str) -> int:
        # is this needed?
        return 0


def isfloat(num) -> bool:
    """ Self-made function to check is string is a float """
    try:
        float(num)
        return True
    except:
        return False


def checknum(num) -> str:
    """ Returns type of ID """
    if num.isnumeric():
        # is an int
        return "integer"

    elif isfloat(num):
        # is a float
        return "float"

    elif num.isalpha():
        # is a variable, access the symbol table
        return "symbol"

    else:
        # uh oh, shouldn't get here. Throw error
        return None