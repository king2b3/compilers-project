''' Holds the syntax structure for the language.

    Created on: 1-29-2021
    Version: Python 3.8.5
    Created by: Bayley King (https://github.com/king2b3)
'''

from main import Compiler
from scanner import Scanner
from tokens import *
from global_params import *

class Parser(Compiler):
    ''' Class for the parser. Contains methods needed for parse, and calls the scanner.
    '''    
    def __init__(self, filename, print_bool=False, error_file='error_log.txt') -> None:
        self.s = Scanner(filename)
        self.current_token = None
        self.next_token = None

        while self.current_token == None:
            self.nextToken()

    def nextToken(self) -> None:
        ''' Gets the next token for current and next self variables
        '''
        self.current_token = self.next_token
        self.next_token = s.getToken()
    
    def checkToken(self, check_token) -> bool:
        ''' Checks if the current token is the same as the expected token
        '''
        return check_token == self.current_token.text

    def checkPeek(self, check_token) -> bool:
        ''' Checks if the next token is the same as the expected token
        '''
        return check_token == self.next_token.text

    def match(self, check_token) -> bool:
        ''' Checks if the next token is the same as the expected token
            Throws error is match fails
        '''
        if not self.checkToken(checkToken):
            message = (f"{bcolors['FAIL']}ERROR: Unexpected token {bcolors['BOLD']}{self.current_token}{bcolors['ENDC']}"
                    f"{bcolors['FAIL']} on line number {bcolors['UNDERLINE']}{s.line_counter + 1}{bcolors['ENDC']}"
                    f"{bcolors['FAIL']}. {check_token} expected.{bcolors['ENDC']}"))           
            self.reportError(message)
    
    #### Parsing Statements ####

    def program(self) -> None:
        ''' <program> ::= 
                <program_header><program_body>.
        '''
        pass
    
    def program_header(self) -> None:
        ''' <program> ::= 
                program <identifer> is
        '''
        pass

    def program_body(self) -> None:
        ''' <program_body> ::= 
                        ( <decleration> ; )*
                    begin
                        ( <statement> : )*
                    end program
        '''
        pass
    
    def decleration(self) -> None:
        ''' <decleration> ::=
                  [global] <procedure_decleration>
                | [global] <variable_decleration> 
                | [global] <type_decleration>
        '''
        pass
    
    def procedure_decleration(self) -> None:
        ''' <procedure_decleration> ::=
                <procedure_header><procedure_body>
        '''
        pass

    def procedure_header(self) -> None:
        ''' <procedure_header> ::=
                procedure <identifier> : <type_mark> ( [<parameter_list>] )
        '''
        pass
    
    def parameter_list(self) -> None:
        ''' <parameter_list> ::=
                  <parameter>,<parameter_list>
                | <parameter>
        '''
        pass
    
    def parameter(self) -> None:
        ''' <parameter> ::=
                <variable_decleration>
        '''
        pass
    
    def procedure_body(self) -> None:
        ''' <procedure_body> ::=
                    ( <decleration> ; )*
                begin
                    (<statement>)*
                end procedure
        '''
        pass
    
    def variable_decleration(self) -> None:
        ''' <variable_decleration> ::=
                variable <identifier> : <type_mark> [[<bound>]]
        '''
        pass
    
    def type_decleration(self) -> None:
        ''' <type_decleration> ::=
                type <identifier> is <type_mark>
        '''
        pass
    
    def type_mark(self) -> None:
        ''' <type_mark> ::=
                  integer | float | string | bool
                | <identifier>
                | enum {<identifier> ( , <identifier> )* }
        '''
        pass
    
    def bound(self) -> None:
        ''' <bound> ::=
                <number>
        '''
        pass
    
    def statement(self) -> None:
        ''' <statement> ::=
                  <assignment_statement>
                | <if_statement>
                | <loop_statement>
                | <return_statement>
        '''
        pass

    def procedure_call(self) -> None:
        ''' <procedure_call> ::=
                <identifier> ( [<argument_list>] )
        '''
        pass
    
    def assignment_statement(self) -> None:
        ''' <assignment_statement> ::=
                <destination> := <expression>
        '''
        pass
    
    def destination(self) -> None:
        ''' <destination> ::=
                <identifier> [[<expression>]]
        '''
        pass
    
    def if_statement(self) -> None:
        ''' <if_statement> ::=
                if (<expression>) then (<statement> ;)*
                [else ( <statement> ; )*]
                end if
        '''
        pass

    def loop_statement(self) -> None:
        ''' <loop_statement> ::=
                for ( <assignment_statement> ; <expression> )
                    ( <statement> ;)*
                end for
        '''
        pass
    
    def return_statement(self) -> None:
        ''' <return_statement> ::=
                return <expression>
        '''
        pass

    def identifier(self) -> None:
        ''' <identifier> ::=
                [a-zA-Z] [a-zA-Z0-9_]*
        '''
        pass
    
    def expression(self) -> None:
        ''' <expression> ::=
                  <expression> & <arithOp>
                | <expression> | <arithOp>
                | [not] <arithOp>
        '''
        pass

    def arithOp(self) -> None:
        ''' <arithOp> ::=
                  <arithOp> + <relation>
                | <arithOp> - <relation>
                | <relation>
        '''
        pass
    
    def relation(self) -> None:
        ''' <relation> ::=
                  <relation> < <term>
                | <relation> > <term>
                | <relation> >= <term>
                | <relation> <= <term>
                | <relation> == <term>
                | <relation> != <term>
                | <term>
        '''
        pass

    def term(self) -> None:
        ''' <term> ::=
                  <term> * <factor>
                | <term> / <factor>
                | <factor>
        '''
        pass

    def factor(self) -> None:
        ''' <factor> ::=
                  (<expression>)
                | <procedure_call>
                | [-] <name>
                | [-] <number>
                | <string>
                | true
                | false
        '''
        pass

    def name(self) -> None:
        ''' <name> ::=
                <identifier> [ [<expression>] ]
        '''
        pass

    def argument_list(self) -> None:
        ''' <argument_list> ::=
                  <expression> , <argument_list>
                | <expression>
        '''
        pass
    
    def number(self) -> None:
        ''' <number> ::=
                [0-9][0-9_]*[.[0-9_]*]
        '''
        pass

    def string(self) -> None:
        ''' <string> ::=
                "[^"]*"
        '''
        pass