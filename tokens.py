''' Definitions file for parser
    Reserved words as a list as well

    Token class can be called to check dictionary

    Created on: 1-15-2021
    Version: Python 3.8.5
    Created by: Bayley King (https://github.com/king2b3)
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
    '"': 'Quote',
    ',': 'Comma'
}

class Token(object):
    ''' Base token class. Parent class for ID and Keyword.

        Not sure if it will turn abstract at some point
    '''
    def __init__(self, text) -> None:
        self.text = text

    def __str__(self) -> str:
        return self.text

class S_Token(Token):
    ''' Child class from Token for symbol tokens.
    '''
    def __init__(self, text) -> None:
        super().__init__(text)
        self.kind = token_type[text]

class ID(Token):
    ''' Child class from Token for the ID token.
    '''
    def __init__(self, text) -> None:
        super().__init__(text)
        self.kind = 'ID'

class Keyword(Token):
    ''' Child class from Token for the Keyword token.
    '''
    def __init__(self, text) -> None:
        super().__init__(text)
        self.kind = 'Keyword'

class Literal(Token):
    ''' Child class from Token for the Literal token.
    '''
    def __init__(self, text) -> None:
        super().__init__(text)
        self.kind = 'Literal'