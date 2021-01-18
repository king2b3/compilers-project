'''
    Scanner aspect of the parser project.
    
    Bayley King
'''

from main import Compiler
from tokens import token_type, reserved_words

class Scanner():
    def __init__(
        self, filename
    ):
        self.line_counter = 0
        self.error_status = None
        self.f = open(filename, 'r').readlines()
        self.current_pos = -1
        self.current_char = ''
        self.scanner_file_name = 'tempFiles/temp_scanner.txt'
        self.nextChar()
      
    def nextChar(
        self
    ) -> str:
        ''' Moves onto the next character in the string
        '''
        self.current_pos += 1
        # make sure we don't look past the length of the string
        if self.current_pos >= len(self.f[self.line_counter]):
            self.current_char = '\0' # End of line
        else:
            self.current_char = self.f[self.line_counter[self.current_pos]]
        
    def peek(
        self
    ) -> str:
        ''' Look at the next character in the line
        '''

        if self.current_pos + 1 >= len(self.f[self.line_counter]):
            return '\0' # End of line
        else:
            return self.f[self.line_counter[self.current_pos]]

    def getToken(
        self
    ) -> str:
        ''' Gets the next token in a string
        '''
        token = None

        if isLetter(self.current_char):
            token = self.current_char
            while isNum(self.peek()) or isLetter(self.peek()):
                self.nextChar()
                token += self.current_char
            if token in reserved_words:
                token = (token,'keyword')  
            else:
                token = (token,'ID')
            
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
                    message = 'Illegal character in number ' + self.line_counter
                    Compiler.reportError(message)
                while self.peek().isdigit():
                    self.nextChar()
                    token += self.current_char
                token = (token,'ID')

        elif isNewLine(self.current_char):
            Compiler.line_counter += 1
            self.current_pos = -1
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
            else:
                token = (self.current_char,token_type[self.current_char])
        
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
            token = (self.current_line,token_type[self.current_char])

        else:
            error_msg = 'Unknown token: ' + self.current_char
            Compiler.reportError(error_msg)
            pass
            # Unknown token
        return token

    # archive? Nor sure if I can use regex, and anyway not worth using it
    '''
    def originalScan(
        self
    ) -> list:
        # Scans the file for tokens.

        #    Uses the regex library

        #    Returns a list of lists, each list is the corresponding line of tokens from the file
        
        import re

        for line in self.f:
            Compiler.line_counter += 1
            temp = line.rstrip()
            temp = re.split(r'(\W+)',temp)
            temp = [elem.strip() for elem in temp if elem not in ['','\t','\n',' ']] 
            for t in range(len(temp)):
                if temp[t] == ');':
                    temp[t] = ')'
                    temp.append(';')
    '''

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