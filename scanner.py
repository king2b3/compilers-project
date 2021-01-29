'''
    Scanner aspect of the parser project.
    
    Bayley King
'''

import pickle as pkl
import csv
from main import Compiler
from tokens import token_type, reserved_words

class Scanner(Compiler):
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
        self.writeToken(token)
        while token != ('Keyword','EOF'): 
            token = self.getToken()
            if token != None:
                self.writeToken(token)
        pkl.dump(self.pickle_scan,open(self.pickle_out_name,'wb'))
        with open(self.text_out_name,"w") as f:
            wr = csv.writer(f)
            wr.writerows(self.pickle_scan)
        if self.print_bool: print('Scanning finished scanning. Scanned results written to file')
    
    def writeToken(self, token) -> None:
        ''' Writes the token to a file, and appends it to a list to be used in pickle
              Tokens can be printed too, based off of initial args parsed into the system
        '''
        try:
            self.pickle_scan[self.line_counter].append(token)
        except: 
            self.pickle_scan[self.line_counter - 1].append(token)
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
        while isNewLine(self.current_char) or isWhiteSpace(self.current_char):
            if isNewLine(self.current_char):
                self.line_counter += 1
                self.nextChar()

            if isWhiteSpace(self.current_char):
                self.nextChar()
                while isWhiteSpace(self.current_char):
                    self.nextChar()

    def eatComments(self, token=None) -> None:    
        ''' Eats whitespace
        '''
        if isComment(self.current_char):
            if self.peek() == '*': # multiline comment
                self.nextChar()
                comment_not_ended = True
                num_blocks = 0
                while comment_not_ended and num_blocks == 0:
                    comment_not_ended = True
                    self.nextChar()
                    if checkEOF(self.current_char): 
                        error_msg = 'Block comment not ended on line' + str(self.line_counter +1)
                        self.reportWarning(error_msg)
                        token = ('Keyword','EOF')
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
                    if checkEOF(self.current_char): 
                        token = ('Keyword','EOF')
                        comment_not_ended = False
                    self.nextChar()
                    if isNewLine(self.current_char):
                        self.line_counter += 1
                        #self.nextChar()
                        comment_not_ended = False
            self.nextChar()
            return token
    
    def getToken(self) -> tuple:
        ''' Gets the next token in a string
        '''
        token = None

        self.eatWhiteSpace()
        token = self.eatComments()

        if self.current_char == '\0':
            token = ('Keyword','EOF')        
                
        elif isSpecialArithOp(self.current_char): # might be able to remove
            if (self.peek() == '+' and self.current_char == '+') or \
                    (self.peek() == '-' and self.current_char == '-'):
                last_char = self.current_char
                self.nextChar()
                token = (token_type[last_char + self.current_char],last_char+self.current_char)
                self.nextChar()
            else:
                token = (token_type[self.current_char],self.current_char)
                self.nextChar()
 
        elif isSpecialEqualToken(self.current_char):
            if self.peek() == '=':
                last_char = self.current_char
                self.nextChar()
                token = (token_type[last_char + self.current_char],last_char+self.current_char)
                self.nextChar()
            else:
                token = (token_type[self.current_char],self.current_char)
                self.nextChar()

        elif isString(self.current_char):
            token = self.current_char
            while self.peek() != '"':
                self.nextChar()
                token += self.current_char
            self.nextChar()
            token += self.current_char  
            self.nextChar()
            token = ('Literal',token)
        
        elif isSingleCharSymbol(self.current_char):
            token = (token_type[self.current_char],self.current_char)
            self.nextChar()
        
        elif isLetter(self.current_char):
            token = self.current_char
            while isNum(self.peek()) or isLetter(self.peek()) or self.peek() == '_':
                self.nextChar()
                token += self.current_char
            token = token.lower()
            if token in reserved_words:
                token = ('Keyword',token)  
            else:
                token = ('ID',token)
            self.nextChar()
            
        elif isNum(self.current_char):
            # check for int / float OR raise exception if decimal isn't correctly written
            token = self.current_char
            while self.peek().isdigit():
                self.nextChar()
                token += self.current_char
            if self.peek() == '.':
                self.nextChar()
                token += self.current_char
                if not self.peek().isdigit():
                    # makes sure that there is at least one floating point after decimal
                    message = 'Illegal character in line number ' + str(self.line_counter +1)
                    Compiler.reportError(message)
                while self.peek().isdigit():
                    self.nextChar()
                    token += self.current_char
            token = ('ID',token)
            self.nextChar()

        else:
            error_msg = 'Unknown token:' + self.current_char + \
                ' on line ' + str(self.line_counter +1)
            self.reportError(error_msg)
            self.nextChar()
            # Unknown token
        return token


def checkEOF(char) -> bool:
    return char == '\0'

def isString(char) -> bool:
    return char == '"'

def isLetter(char) -> bool:
    return char.isalpha()

def isNum(char) -> bool:
    return char.isnumeric()

def isSpecialEqualToken(char) -> bool:
    return char == '>' or char == '<' or char == '!' or char == ':' or char == '='

def isSingleCharSymbol(char) -> bool:
    return char in token_type.keys()

def isSpecialArithOp(char) -> bool:
    return char == '+' or char == '-'

def isWhiteSpace(char) -> bool:
    return char == '\t' or char == ' ' or char == '\r'

def isComment(char) -> bool:
    return char == '/'

def isNewLine(char) -> bool:
    return char == '\n'