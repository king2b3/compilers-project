""" Holds the symbol table structure for the language.

    Created on: 1-29-2021
    Version: Python 3.8.5
    Created by: Bayley King (https://github.com/king2b3)
"""

# Make the attributes a dictionary? Then we could add whatever we would like to them.
class SymbolTable(object):
    def __init__(self, print_bool=False ) -> None:
        self.table = {}

    def allocate(self, symbol) -> object:
        """ Allocates a new empty symbol table. """
        self.table[symbol] = SymbolTable()
    
    def free(self) -> None:
        """ Removes all the entries of a table. """
        pass
    
    def lookup(self, name) -> object:
        """ Returns the reference to the symbol's class. """
        pass
    
    def insert(self, symbol, symbol_type) -> None:
        """ Adds a symbol to the table. If symbol is already in the table, pass. """
        # checks if symbol is in the table 
        if symbol in self.table:
            pass
        else:
            self.table[symbol] = symbol_type
    
    def set_attribute(self, name, attr) -> None:
        """ Sets an attribute for a given entry. """
        pass

    def get_attribute(self, name) -> None:
        """ Returns an attribute. Just not sure what the type of an attribute is yet.
        """
        pass

