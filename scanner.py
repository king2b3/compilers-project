''' Holds the scanner structure for the front end of the compiler.

    Created on: 1-15-2021
    Version: Python 3.8.5
    Created by: Bayley King (https://github.com/king2b3)
'''

from main import Compiler
#from tokens import token_type, reserved_words, Token, ID, Keyword
from tokens import *

class Scanner(Compiler):
    ''' Scanner class. Holds methods to get tokens and scan/lex the input file. 
    '''
    def __init__(self, filename, print_bool=False, error_file='error_log.txt') -> None:
        self.line_counter = 0
        self.error_file = error_file
        self.error_status = None
        self.f = open(filename, 'r').readlines()
        self.total_lines = len(self.f)
        self.f = ''.join(map(str, self.f))
        self.current_pos = -1
        self.current_char = ''
        self.text_out_name = 'tempFiles/temp_scanner.txt'
        self.pickle_out_name = 'tempFiles/temp_scanner.pkl'
        self.pickle_scan = [ [] for t in range(self.total_lines) ]
        self.print_bool = print_bool
        self.nextChar()

    def scanFile(self) -> None:
        ''' Scans file and writes tokens to text and pickle file
        '''
        if self.print_bool: print('Scanning file now....')
        token = self.getToken()
        if token != None:
            text = token.text
            self.writeToken(token)
        else:
            text = ''
        self.writeToken(token)
        while text != 'EOF': 
            token = self.getToken()
            if token != None:
                text = token.text
                self.writeToken(token)
        if self.print_bool: print('Scanning finished scanning. Scanned results written to file')
    
    def writeToken(self, token) -> None:
        ''' Writes the token to a file, and appends it to a list to be used in pickle
              Tokens can be printed too, based off of initial args parsed into the system
        '''
        if self.print_bool: print(token)
    
    def nextChar(self) -> None:
        ''' Moves onto the next character in the string
        '''
        self.current_pos += 1
        # make sure we don't look past the length of the string
        if self.current_pos >= len(self.f):
            self.current_char = '\0' # End of line
        else:
            self.current_char = self.f[self.current_pos]
        
    def peek(self) -> str:
        ''' Look at the next character in the line
        '''

        if self.current_pos + 1 >= len(self.f):
            return '\0' # End of line
        else:
            return self.f[self.current_pos+1]

    def eatWhiteSpace(self) -> None:
        ''' Eats all whitespace
        '''
        while self.current_char == ' ' or self.current_char == '\t' or self.current_char == '\r':
            self.nextChar()
                
    def eatComments(self, token=None) -> None:    
        ''' Eats comments
        '''
        while self.current_char == '/' and (self.peek() == '*' or self.peek() == '/'):
            if self.peek() == '*': # multiline comment
                self.nextChar()
                comment_not_ended = True
                num_blocks = 1
                while comment_not_ended or num_blocks != 0:
                    comment_not_ended = True
                    self.nextChar()
                    if self.current_char == '\0': 
                        error_msg = 'Block comment not ended on line' + str(self.line_counter +1)
                        self.reportWarning(error_msg)
                        self.current_char = '\0'
                        comment_not_ended = False 
                        num_blocks = 0
                    if self.current_char == '*' and self.peek() == '/':
                        self.nextChar()
                        num_blocks -= 1
                        comment_not_ended = False
                    elif self.current_char == '/' and self.peek() == '*':
                        num_blocks += 1

            elif self.peek() == '/': #  single line comment 
                self.nextChar()
                comment_not_ended = True
                while comment_not_ended:
                    self.nextChar()
                    if self.current_char == '\0': 
                        comment_not_ended = False
                    if self.current_char == '\n':
                        self.line_counter += 1
                        comment_not_ended = False
    
    def getToken(self) -> tuple:
        ''' Gets the next token in a string
        '''
        token = None
        
        self.eatWhiteSpace()
        self.eatComments()
        
        while self.current_char == '/': # 
            self.nextChar()
            self.eatComments()
            self.eatWhiteSpace()

        if self.current_char == '\0':
            token = Keyword('EOF')        
        
        elif self.current_char == '\n':
            self.line_counter += 1
            self.nextChar()

        elif self.current_char == '>' or self.current_char == '<' or self.current_char == '!' \
                    or self.current_char == ':' or self.current_char == '=':
            if self.peek() == '=':
                last_char = self.current_char
                self.nextChar()
                token = Token(last_char+self.current_char)                
                self.nextChar()
            else:
                token = Token(self.current_char)
                self.nextChar()

        elif self.current_char == '"':
            token = self.current_char
            while self.peek() != '"':
                self.nextChar()
                token += self.current_char
            self.nextChar()
            token += self.current_char  
            self.nextChar()
            token = Literal(token)
        
        elif self.current_char in token_type.keys():
            token = S_Token(self.current_char)
            self.nextChar()
        
        elif self.current_char.isalpha():
            token = self.current_char
            while self.peek().isnumeric() or self.peek().isalpha() or self.peek() == '_':
                self.nextChar()
                token += self.current_char
            token = token.lower()
            if token in reserved_words:
                token = Keyword(token)  
            else:
                token = ID(token)
            self.nextChar()
            
        elif self.current_char.isnumeric():
            # check for int / float OR raise exception if decimal isn't correctly written
            token = self.current_char
            while self.peek().isnumeric():
                self.nextChar()
                token += self.current_char
            if self.peek() == '.':
                self.nextChar()
                token += self.current_char
                if not self.peek().isnumeric():
                    # makes sure that there is at least one floating point after decimal
                    message = 'Illegal character in line number ' + str(self.line_counter +1)
                    Compiler.reportWarning(message)
                while self.peek().isdigit():
                    self.nextChar()
                    token += self.current_char
            token = ID(token)
            self.nextChar()

        else:
            error_msg = 'Unknown token:' + self.current_char + \
                ' on line ' + str(self.line_counter)
            self.reportWarning(error_msg)
            self.nextChar()
            # Unknown token

        return token
