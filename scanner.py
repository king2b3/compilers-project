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
        print_bool=False,
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

        def EOF(
            self
        ) -> tuple:
            return ('Keyword','EOF')
            
        def NewLine(
            self
        ) -> None:
            self.line_counter += 1
            self.nextChar()
        
        def WhiteSpace(
            self
        ) -> None:
            self.nextChar()
            while isWhiteSpace(self.current_char):
                self.nextChar()

        def String(
            self
        ) -> tuple:
            token = self.current_char
            while self.peek() != '"':
                self.nextChar()
                token += self.current_char
            self.nextChar()
            token += self.current_char  
            self.nextChar()
            return ('Literal',token)

        def SpecialEquals(
            self
        ) -> tuple:
            if self.peek() == '=':
                last_char = self.current_char
                self.nextChar()
                token = (token_type[last_char + self.current_char],last_char+self.current_char)
                self.nextChar()
            else:
                token = (token_type[self.current_char],self.current_char)
                self.nextChar()
            return token

        def SpecialAdd(
            self
        ) -> tuple:
            if (self.peek() == '+' and self.current_char == '+') or \
                    (self.peek() == '-' and self.current_char == '-'):
                last_char = self.current_char
                self.nextChar()
                token = (token_type[last_char + self.current_char],last_char+self.current_char)
                self.nextChar()
            else:
                token = (token_type[self.current_char],self.current_char)
                self.nextChar()
            return token

        def Comment(
            self
        ) -> None:
            if self.peek() == '*': # multiline comment
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
            self.nextChar()
        
        self.get_token_hash = {
        '\0': EOF,
        '\n': NewLine,
        '\t': WhiteSpace,
        '\r': WhiteSpace,
        ' ': WhiteSpace,
        '"': String,
        '>': SpecialEquals,
        '<': SpecialEquals,
        '!': SpecialEquals,
        ':': SpecialEquals,
        '=': SpecialEquals,
        '+': SpecialAdd,
        '-': SpecialAdd,
        '/': Comment
    } 



    def scanFile(
        self
    ) -> None:
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
    
    def writeToken(
        self, token
    ) -> None:
        ''' Writes the token to a file, and appends it to a list to be used in pickle
              Tokens can be printed too, based off of initial args parsed into the system
        '''
        try:
            self.pickle_scan[self.line_counter].append(token)
        except: 
            self.pickle_scan[self.line_counter - 1].append(token)
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
    ) -> tuple:
        ''' Gets the next token in a string
        '''
        token = None

        try:
            print('pass')
            self.get_token_hash[self.current_char]()
        except:

            if self.current_char in token_type:
                token = (token_type[self.current_char],self.current_char)
                self.nextChar()
            
            elif self.current_char.isalpha():
                token = self.current_char
                while self.peek().isalpha() or self.peek().isalpha() or self.peek() == '_':
                    self.nextChar()
                    token += self.current_char
                token = token.lower()
                if token in reserved_words:
                    token = ('Keyword',token)  
                else:
                    token = ('ID',token)
                self.nextChar()
                
            elif self.current_char.isdigit():
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