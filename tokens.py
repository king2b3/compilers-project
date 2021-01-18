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
    'not'
]

token_type = {
    '+': 'symbol',
    '-': 'symbol',
    '<': 'symbol',
    '<=': 'symbol',
    '>': 'symbol',
    '>=': 'symbol',
    ':=': 'symbol',
    '==': 'symbol',
    '!=': 'symbol',
    '&': 'symbol',
    '|': 'symbol',
    '*': 'symbol',
    '/': 'symbol',
    ':': 'symbol',
    '(': 'symbol',
    ')': 'symbol',
    ';': 'symbol',
    '.': 'symbol'
}

