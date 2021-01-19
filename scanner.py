'''
    Scanner aspect of the parser project.
    
    Bayley King
'''

import pickle as pkl
import csv
from main import Compiler
from tokens import token_type, reserved_words

class Scanner(Compiler):
    def __init__(
        self, filename,
        print_bool = False,
        error_file='error_log.txt'
    ):
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

    def scanFile(
        self
    ) -> None:
        ''' Scans file and writes tokens to text and pickle file
        '''
        if self.print_bool: print('Scanning file now....')
        token = self.getToken()
        self.writeToken(token)
        while token != ('EOF','keyword'): 
            token = self.getToken()
            if token != None:
                self.writeToken(token)
        pkl.dump(self.pickle_scan,open(self.pickle_out_name,'wb'))
        with open(self.text_out_name,"w") as f:
            wr = csv.writer(f)
            wr.writerows(self.pickle_scan)
        if self.print_bool: print('Scanning finished scanning. Scanned results written to file')
    
    def writeToken(
        self, token
    ) -> None:
        ''' Writes the token to a file, and appends it to a list to be used in pickle
              Tokens can be printed too, based off of initial args parsed into the system
        '''
        self.pickle_scan[self.line_counter].append(token)
        if self.print_bool: print(token)
    
    def nextChar(
        self
    ) -> None:
        ''' Moves onto the next character in the string
        '''
        self.current_pos += 1
        # make sure we don't look past the length of the string
        if self.current_pos >= len(self.f):
            self.current_char = '\0' # End of line
        else:
            self.current_char = self.f[self.current_pos]
        
    def peek(
        self
    ) -> str:
        ''' Look at the next character in the line
        '''

        if self.current_pos + 1 >= len(self.f):
            return '\0' # End of line
        else:
            return self.f[self.current_pos+1]

    def getToken(
        self
    ) -> str:
        ''' Gets the next token in a string
        '''
        token = None

        if self.current_char == '\0':
            return ('EOF','keyword')        
        elif isNewLine(self.current_char):
            self.line_counter += 1
            self.nextChar()

        elif isWhiteSpace(self.current_char):
            self.nextChar()
            while isWhiteSpace(self.current_char):
                self.nextChar()
        
        elif isSpecialEqualToken(self.current_char):
            if self.peek() == '=':
                last_char = self.current_char
                self.nextChar()
                token = (last_char+self.current_char,token_type[last_char + self.current_char])
                self.nextChar()
            else:
                token = (self.current_char,token_type[self.current_char])
                self.nextChar()
        
        elif isComment(self.current_char):
            if self.peak() == '*': # multiline comment
                self.nextChar()
                comment_not_ended = True
                while comment_not_ended:
                    self.nextChar()
                    if self.current_char == '*' and self.peek() == '/':
                        self.nextChar()
                        comment_not_ended = False
            elif self.peek() == '/': #  single line comment 
                self.nextChar()
                comment_not_ended = True
                while comment_not_ended:
                    self.nextChar()
                    if self.current_char == '\n':
                        self.nextChar()
                        comment_not_ended = False

        elif self.current_char in token_type.keys():
            token = (self.current_char,token_type[self.current_char])
            self.nextChar()
        
        elif isLetter(self.current_char):
            token = self.current_char
            while isNum(self.peek()) or isLetter(self.peek()):
                self.nextChar()
                token += self.current_char
            if token in reserved_words:
                token = (token,'keyword')  
            else:
                token = (token,'ID')
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
                    message = 'Illegal character in number ' + str(self.line_counter +1)
                    Compiler.reportError(message)
                while self.peek().isdigit():
                    self.nextChar()
                    token += self.current_char
            token = (token,'ID')
            self.nextChar()

        else:
            error_msg = 'Unknown token:' + self.current_char + \
                ' on line ' + str(self.line_counter +1)
            self.reportError(error_msg)
            self.nextChar()
            # Unknown token
        return token


def isLetter(
    char
) -> bool:
    return char.isalpha()

def isNum(
    char
) -> bool:
    return char.isnumeric()

def isSpecialEqualToken(
    char
) -> bool:
    return char == '>' or char == '<' or char == '!' or char == ':' or char == '='

def isWhiteSpace(
    char
) -> bool:
    return char == '\t' or char == ' ' or char == '\r'

def isComment(
    char
) -> bool:
    return char == '/'

def isNewLine(
    char
) -> bool:
    return char == '\n'