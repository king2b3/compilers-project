'''
    Definitions file for parser
    Reserved words as a list as well

    Token class can be called to check dictionary
'''

reserved_words = [
    'return',
    'end',
    'if',
    'else',
    'then',
    'true',
    'false',
    'while',
    'for',
    'begin',
    'end',
    'program',
    'global',
    'procedure',
    'variable',
    'integer',
    'float',
    'string',
    'bool',
    'enum',
    'not',
    'is',
    'EOF',
    'enum',
    'getbool',
    'getinteger',
    'getfloat',
    'getstring',
    'putbool',
    'putinteger',
    'putfloat',
    'putstring',
    'sqrt'
]

token_type = {
    # (Speech, Token_Type)
    '+': 'ArithOp',
    '-': 'ArithOp',
    '++': 'ArithOp',
    '--': 'ArithOp',
    '<': 'Relation',
    '<=': 'Relation',
    '>': 'Relation',
    '>=': 'Relation',
    ':=': 'Relation',
    '==': 'Relation',
    '!=': 'Relation',
    '&': 'Expression',
    '|': 'Expression',
    '*': 'Term',
    '/': 'Term',
    ':': 'Colon',
    '(': 'LeftPar',
    ')': 'Rightpar',
    ';': 'Semicolon',
    '.': 'Period',
    '[': 'LeftBracket',
    ']': 'RightBracket',
    '"': 'quote',
    ',': 'comma'
}


# Make the attributes a dictionary? Then we could add whatever we would like to them.
class SymbolTable(object):
    def __init__(
        self,
        print_bool=False 
    ):
        self.table = {}

    def allocate(
        self, symbol
    ) -> object:
        ''' Allocates a new empty symbol table
        '''
        self.table[symbol] = SymbolTable()
    
    def free(
        self
    ) -> None:
        ''' Removes all the entries of a table
        '''
        None
    
    def lookup(
        self, name
    ) -> object:
        ''' Returns the reference to the symbol's class
        '''
        None
    
    def insert(
        self, symbol,
        symbol_type
    ) -> None:
        ''' Adds a symbol to the table. If symbol is already in the table, pass.
        '''
        # checks if symbol is in the table 
        if symbol in self.table:
            pass
        else:
            self.table[symbol] = symbol_type
    
    def set_attribute(
        self, name,
        attr
    ) -> None:
        ''' Sets an attribute for a given entry
        '''
        None

    def get_attribute(
        self, name
    ) -> None:
        ''' Returns an attribute. Just not sure what the type of an attribute is yet.
        '''

