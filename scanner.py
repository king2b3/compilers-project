""" Holds the scanner structure for the front end of the compiler.

    Created on: 1-15-2021
    Version: Python 3.8.5
    Created by: Bayley King (https://github.com/king2b3)
"""

from main import Compiler
from tokens import *
from global_params import *

class Scanner(Compiler):
    """ Scanner class. Holds methods to get tokens and scan/lex the input file. """
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
        """ Scans file and writes tokens to text and pickle file """
        if self.print_bool: print('Scanning file now....')
        token = Null()
        while token.text != 'EOF': 
            token = self.getToken()
            self.writeToken(token)
        if self.print_bool: print('Scanning finished scanning. Scanned results written to file')
    
    def writeToken(self, token) -> None:
        """ Prints tokens, just for debug purposes. """
        if self.print_bool: print(token)
    
    def nextChar(self) -> None:
        """ Moves onto the next character in the input file """
        self.current_pos += 1
        # make sure we don't look past the length of the string
        if self.current_pos >= len(self.f):
            self.current_char = '\0' # End of line
        else:
            self.current_char = self.f[self.current_pos]
        
    def peek(self) -> str:
        """ Look at the next character in the input file """
        if self.current_pos + 1 >= len(self.f):
            # End of line
            return '\0'
        else:
            return self.f[self.current_pos+1]

    def eatWhiteSpace(self) -> None:
        """ Eats all whitespace until next non-whitespace char is found """
        while self.current_char == ' ' or self.current_char == '\t' or self.current_char == '\r':
            self.nextChar()
                
    def eatComments(self, token=None) -> None:    
        """ Eats comments until next non-comment char is found """
        while self.current_char == '/' and (self.peek() == '*' or self.peek() == '/'):
            # multiline comment
            if self.peek() == '*': 
                self.nextChar()
                self.nextChar()
                comment_not_ended = True
                num_blocks = 1
                while comment_not_ended or num_blocks != 0:
                    comment_not_ended = True
                    self.nextChar()
                    if self.current_char == '\0': 
                        # Multiline comment not ended before EOF
                        error_msg = 'Multiline comment not ended on line' + str(self.line_counter +1)
                        self.reportWarning(error_msg)
                        self.current_char = '\0'
                        comment_not_ended = False 
                        num_blocks = 0
                    if self.current_char == '*' and self.peek() == '/':
                        # End of a nested multiline
                        self.nextChar()
                        num_blocks -= 1
                        comment_not_ended = False
                    elif self.current_char == '/' and self.peek() == '*':
                        # New nested multiline found
                        num_blocks += 1
                        self.nextChar()
                        self.nextChar()
                self.nextChar()

            elif self.peek() == '/':  
                # Single line comment found
                self.nextChar()
                comment_not_ended = True
                while comment_not_ended:
                    self.nextChar()
                    if self.current_char == '\0': 
                        comment_not_ended = False
                    if self.current_char == '\n':
                        self.line_counter += 1
                        comment_not_ended = False
    
    def getToken(self) -> "Token":
        """ Gets the next token in the input file.
            Returns:
              Some child of the token class if the token is a real value.
              On some instances, type None can be returned.
              Parser should check if returned token = None, if so call func again.
        """
        # inits blank token class 
        token = Null()
        
        # removes all white space and comments 
        while ((self.current_char == '/' and (self.peek() == '*' or self.peek() == '/')) or
                self.current_char == ' ' or self.current_char == '\t' or self.current_char == '\r'):
            self.eatWhiteSpace()
            self.eatComments()
    
        # Conditional for token types
        if self.current_char == '\0':
            """ End of File """
            token = Keyword('EOF')        
        
        elif self.current_char == '\n':
            """ New line """
            self.line_counter += 1
            self.nextChar()
            token = self.getToken()

        elif self.current_char == '>' or self.current_char == '<' or self.current_char == '!' or
                self.current_char == ':' or self.current_char == '=':
            """ Relation tokens """
            if self.peek() == '=':
                # Two character tokens
                last_char = self.current_char
                self.nextChar()
                token = Token(last_char+self.current_char)                
                self.nextChar()
            else:
                # Single character tokens
                token = Token(self.current_char)
                self.nextChar()

        elif self.current_char == '"':
            """ Strings """
            # not the proper way to do this, but eh wanted to save on some variable names
            token = self.current_char
            while self.peek() != '"':
                # saves characters until end of string is found
                self.nextChar()
                token += self.current_char
            self.nextChar()
            token += self.current_char  
            self.nextChar()
            token = String(token)
        
        elif self.current_char in token_type.keys():
            """ Single Character Characters """
            token = S_Token(self.current_char)
            self.nextChar()
        
        elif self.current_char.isalpha():
            """ Reserved words or variables """
            token = self.current_char
            while self.peek().isnumeric() or self.peek().isalpha() or self.peek() == '_':
                # saves characters until end of word if found
                self.nextChar()
                token += self.current_char
            token = token.lower()
            if token in reserved_words:
                token = Keyword(token)  
            else:
                token = ID(token)
            self.nextChar()
            
        elif self.current_char.isnumeric():
            """ Numerical variables """
            token = self.current_char
            while self.peek().isnumeric():
                # saves characters until end of numeric is found
                self.nextChar()
                token += self.current_char
            # for floating point values only. Send type info here?
            if self.peek() == '.':
                self.nextChar()
                token += self.current_char
                # makes sure that there is at least one floating point after decimal
                if not self.peek().isnumeric():
                    message = (f"{bcolors['WARNING']}WARNING: Unknown character {bcolors['BOLD']}{self.current_char}{bcolors['ENDC']}"
                            f"{bcolors['WARNING']}. Digit expected in float "
                            f"on line number {bcolors['UNDERLINE']}{self.line_counter + 1}{bcolors['ENDC']}")
                    Compiler.reportWarning(message)
                while self.peek().isdigit():
                    # saves characters until end of numerical is found 
                    self.nextChar()
                    token += self.current_char
            token = ID(token)
            self.nextChar()

        else:
            """ Not in other cases. Unknown character """
            message = (f"{bcolors['WARNING']}WARNING: Unknown token {bcolors['BOLD']}{self.current_char}{bcolors['ENDC']}"
                    f"{bcolors['WARNING']} on line number {bcolors['UNDERLINE']}{self.line_counter + 1}{bcolors['ENDC']}") 
            self.reportWarning(message)
            self.nextChar()
            # Unknown token
        
        return token

def main(input_file='compiler_theory_test_programs/correct/source.src'):
    """ For testing purposes only """
    from os import system
    system("clear")
    s = Scanner(input_file,True)
    #print(s.f)
    s.scanFile()

if __name__ == "__main__":
    main()