''' Holds the syntax structure for the language.

    Created on: 1-29-2021
    Version: Python 3.8.5
    Created by: Bayley King (https://github.com/king2b3)
'''

import abc


class Syntax(abc.ABC):
    def __init__(self) -> None:
        ''' Abstract class to hold the syntax of the programming language
        '''
        pass
    
    @abc.abstractmethod
    def checkRules(self) -> bool:
        ''' Checks for errors for the syntax of the 
        '''
        pass

    @abc.abstractmethod
    def 