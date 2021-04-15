""" Holds the symbol table structure for the language.
    
    SymbolTable holds two instances of the table object, one for global one for local
      Global is defined once and never changed, local is reset frequently
    
    Although this isn't the best representation, this grammar is simple enough to just allow
      a global and local symbol table.

    Created on: 1-29-2021
    Version: Python 3.8.5
    Created by: Bayley King (https://github.com/king2b3)
"""

from collections import defaultdict
import time

def def_value():
    return None

class SymbolTable(object):
    def __init__(self) -> None:
        self.global_table = Table()
        # local tables are a looked at like a stack. pop and append list to act like a stack
        self.local_table = []

    def lookup(self) -> str:
        """ Looks through tables (based off of current location)

            Returns None if the entry doesn't exist
        """
        if self.global_table.lookup() != None:
            # variable exists in the global table
            ...
        elif self.local_table.lookup() != None:
            # variable exists in the local table
            ...
        else:
            # variable isn't defined
            ...
    
    def insert(self, name:str, symbol_type:str, table_type:bool) -> int:
        """ Checks if the variable already exists in the table

            If not, then it will add the 
        """
        if table_type:
            # Insert into the local table
            if self.local_table.lookup() == None:
                # variable does not exist in the local table
                if self.global_table.lookup() == None:
                    # variable does not exist in the global table
                    # can be added to the local table
                    ...
                else:
                    # variable exists in the global table, but not in the local table
                    ...
            else:
                # variable is already defined
                ...
        else:
            # Insert into the global table
            if self.global_table.lookup() == None:
                self.global_table.insert(name, symbol_type)
                # success
                return 1
            else:
                # failure 
                return 0
                ...

    def append_stack(self, name, symbol_type) -> None:
        """ Creates a new local table, appends onto list 
        """
        self.local_table.append(Table())
        self.local_table[-1].insert(name, symbol_type)
    
    def pop_stack(self) -> None:
        """ Pops the local table off of the stack
        """
        self.local_table.pop()
    
    def __str__(self) -> str:
        temp_str = f"Global Symbol Table: \n"
        temp_str += self.global_table.__str__()
        for i in self.local_table:
            temp_str += '\n'
            temp_str += f"Local Symbol Table: \n"
            temp_str += i.__str__()
        return temp_str


class Table(object):
    def __init__(self) -> None:
        self.table = defaultdict(def_value)

    def lookup(self, name) -> str:
        """ Will return None if the entry doesn't exist """
        return self.table[name]
    
    def insert(self, symbol, symbol_type) -> None:
        """ Adds a symbol to the table. If symbol is already in the table, pass """
        self.table[symbol] = symbol_type
    
    def __str__(self) -> str:
        """ Printed representation of the table """
        temp_str = ""
        for entry in self.table:
            temp_str += f"{entry}:{self.table[entry]}\n"
        temp_str = temp_str.rstrip()
        return temp_str

def main():
    """ For testing purposes only """
    t = SymbolTable()
    t.global_table.insert('a','int')
    t.global_table.insert('c','bool')
    t.local_table.insert('b','int')
    t.local_table.insert('d','str')
    print(t)

if __name__ == "__main__":
    main()