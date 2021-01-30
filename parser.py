''' Holds the syntax structure for the language.

    Created on: 1-29-2021
    Version: Python 3.8.5
    Created by: Bayley King (https://github.com/king2b3)
'''

from main import Compiler
from scanner import Scanner
from tokens import *

class Parser(Compiler):
    ''' Class for the parser. Contains methods needed for parse, and calls the scanner.
    '''    
    def __init__(self, filename, print_bool=False, error_file='error_log.txt') -> None:
        self.s = Scanner(filename)
        self.current_token = None
        self.next_token = None

        while self.current_token == None:
            self.getToken()

    def getToken(self) -> 'Token':
        ''' Gets the next token for current and next
        '''
        self.current_token = self.next_token
        self.next_token = s.getToken()
    
    def checkToken(self, check_token) -> bool:
        ''' Checks if the current token is the same as the expected token
        '''
        return check_token == self.current_token

    def checkPeek(self, check_token) -> bool:
        ''' Checks if the next token is the same as the expected token
        '''
        return check_token == self.next_token
    