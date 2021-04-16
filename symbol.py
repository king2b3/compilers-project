""" Holds the symbol table structure for the language.
    
    SymbolTable holds two instances of the table object, one for global one for local
      Global is defined once and never changed, local is reset frequently
    
    Although this isn't the best representation, this grammar is simple enough to just allow
      a global and local symbol table.

    Created on: 1-29-2021
    Version: Python 3.8.5
    Created by: Bayley King (https://github.com/king2b3)
"""

import time


class SymbolTable(object):
    def __init__(self) -> None:
        self.global_table = Table()
        # local tables are a looked at like a stack. pop and append list to act like a stack
        self.local_table = []

    def lookup(self, name) -> str:
        """ Looks through tables (based off of current location)

            Returns None if the entry doesn't exist
        """
        if (symbol := self.global_table.lookup(name)) != None:
            # variable exists in the global table
            return symbol
        elif len(self.local_table) == 0:
            # Doesn't exist in global, and local doesn't exist yet
            return None
        elif (symbol := self.local_table[-1].lookup(name)) != None:
            # variable exists in the local table
            return symbol
        else:
            # variable isn't defined
            return None
    
    def insert(self, name:str, symbol_type:str, table_type:bool) -> int:
        """ Checks if the variable already exists in the table
        """
        if table_type:
            # try to insert into the local table
            if self.local_table[-1].lookup(name) == None:
                # variable does not exist in the local table
                # it can exist in the global table, but this is a shadow 
                self.local_table[-1].insert(name, symbol_type)
                # success
                return 1
            else:
                # variable is already defined in the local table
                # throws error. redefined variable
                return 0
        else:
            # Try to insert into the global table
            if self.global_table.lookup(name) == None:
                self.global_table.insert(name, symbol_type)
                # success
                return 1
            else:
                # throws error, redefined variable
                # already exists in global table
                return 0
        
        # if the code path somehow gets here, run away screaming
        return 0 

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
        self.table = {}

    def lookup(self, name) -> str:
        """ Will return None if the entry doesn't exist
        """
        return self.table.get(name)
    
    def insert(self, symbol, symbol_type) -> None:
        """ Adds a symbol to the table
        """
        self.table[symbol] = symbol_type
    
    def __str__(self) -> str:
        """ Printed representation of the table 
        """
        temp_str = ""
        for entry in self.table:
            temp_str += f"{entry}:{self.table[entry]}\n"
        temp_str = temp_str.rstrip()
        return temp_str

def main():
    """ For testing purposes only 
    """
    t = SymbolTable()
    t.global_table.insert('a','int')
    print(t)
    
    t.global_table.insert('c','bool')
    print(t)
    
    t.lookup('test')
    print(t)

    
    t.append_stack('b','int')
    t.local_table[-1].insert('d','str')
    
    t.append_stack('e','int')
    t.local_table[-1].insert('f','str')
    print(t)
    
    print(t.lookup('a'))
    print(t.lookup('no'))
    print(t)


if __name__ == "__main__":
    main()