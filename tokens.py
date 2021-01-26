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

class Token(object):
    def __init__(
        self, val,
        children=None
    ):
        self.val = val
        self.children = None

class Program(Token):
    def __init__(
        self, val,
        children=None
    ):
        Token.__init__(val,children)


class Expression(Token):
    def __init__(
        self, val,
        children=None
    ):
        Token.__init__(val,children)


class ArithOp(Token):
    def __init__(
        self, val,
        children=None
    ):
        Token.__init__(val,children)