''' Holds the parser structure for the language.

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

    def matchToken(self, check_token) -> bool:
        ''' Checks if the current token matches the expected token
            Throws error if match fails
        '''
        if not self.checkToken(checkToken):
            message = (f"{bcolors['FAIL']}ERROR: Unexpected token {bcolors['BOLD']}{self.current_token}{bcolors['ENDC']}"
                    f"{bcolors['FAIL']} on line number {bcolors['UNDERLINE']}{s.line_counter + 1}{bcolors['ENDC']}"
                    f"{bcolors['FAIL']}. {check_token} expected.{bcolors['ENDC']}"))           
            self.reportError(message)
        self.nextToken()
    
    def checkType(self, check_token) -> bool:
        ''' Checks if the current token type matches the expected type
        '''
        return check_token == self.current_token.kind

    def matchType(self, check_token) -> bool:
        ''' Checks if the token type is the expected type
            Throws error if matchToken fails
        '''
        if not self.checkType(check_token):
            message = (f"{bcolors['FAIL']}ERROR: Unexpected type {bcolors['BOLD']}{self.current_token.kind}{bcolors['ENDC']}"
                    f"{bcolors['FAIL']} on line number {bcolors['UNDERLINE']}{s.line_counter + 1}{bcolors['ENDC']}"
                    f"{bcolors['FAIL']}. type {check_token} expected.{bcolors['ENDC']}")) 
        self.nextToken()


    ''' Parsing Statements '''

    def program(self) -> None:
        ''' <program> ::= 
                <program_header><program_body>.
        '''
        self.matchToken("program")
        if self.print_bool: print("program")
        # might not need to use a WHILE loop here
        while self.current_token.text != "EOF":
            self.program_header()
            self.program_body()

    def program_header(self) -> None:
        ''' <program_header> ::= 
                program <identifier> : is
        '''
        if self.print_bool: print("program_header")
        self.matchToken("program")
        self.identifier()
        self.matchToken(":")
        self.matchToken("is")

    def program_body(self) -> None:
        ''' <program_body> ::= 
                        ( <decleration> ; )*
                    begin
                        ( <statement> : )*
                    end program
        '''
        if self.print_bool: print("program_body")
        while not self.checkToken("begin"):
            self.decleration()
            self.matchToken(";")
        self.matchToken("begin")
        while not self.checkToken("end"):
            self.statement()
            self.matchToken(";")
        self.matchToken("end")
        self.matchToken("program")
    
    def decleration(self) -> None:
        ''' <decleration> ::=
                  [global] <procedure_decleration>
                | [global] <variable_decleration> 
                | [global] <type_decleration>
        '''
        if self.print_bool: print("decleration")
        if checkToken("global"):
            if print_bool: print("global")
            self.nextToken()
        if checkToken("procedure"):
            self.procedure_decleration()
        elif checkToken("variable"):
            self.variable_decleration()
        else:
            self.type_decleration()
        
    def procedure_decleration(self) -> None:
        ''' <procedure_decleration> ::=
                <procedure_header><procedure_body>
        '''
        if self.print_bool: print("procedure decleration")
        self.procedure_decleration()
        self.procedure_body()

    def procedure_header(self) -> None:
        ''' <procedure_header> ::=
                procedure <identifier> : <type_mark> ( [<parameter_list>] )
        '''
        if self.print_bool: print("procedure header")
        self.matchToken("procedure")
        self.identifier()
        self.matchToken(":")
        self.type_mark()
        self.matchToken("(")
        if not self.checkToken(")"):
            self.parameter_list()
        self.matchToken(")")
    
    def parameter_list(self) -> None:
        ''' <parameter_list> ::=
                  <parameter> , <parameter_list>
                | <parameter>
        '''
        if self.print_bool: print("parameter list")
        self.parameter()
        if self.checkToken(","):
           self.nextToken()
           self.parameter_list()            

    def parameter(self) -> None:
        ''' <parameter> ::=
                <variable_decleration>
        '''
        if self.print_bool: print("parameter")
        self.variable_decleration()
    
    def procedure_body(self) -> None:
        ''' <procedure_body> ::=
                    ( <decleration> ; )*
                begin
                    (<statement>)*
                end procedure
        '''
        if self.print_bool: print("procedure body")
        while not self.checkToken("begin"):
            self.decleration()
            self.matchToken(";")
        self.nextToken()
        while not self.checkToken("end")
            self.statement()
        self.matchToken("end")
        self.matchToken("procedure")

    def variable_decleration(self) -> None:
        ''' <variable_decleration> ::=
                variable <identifier> : <type_mark> [[<bound>]]
        '''
        if self.print_bool: print("variable decleration")
        self.matchToken("variable")
        self.identifier()
        self.matchToken(":")
        self.type_mark()
        if self.checkToken("["):
            self.nextToken()
            self.bound()
            self.checkToken("]")
        
    def type_decleration(self) -> None:
        ''' <type_decleration> ::=
                type <identifier> is <type_mark>
        '''
        if self.print_bool: print("type decleration")
        self.matchToken("type")
        self.identifier()
        self.matchToken("is")
        self.type_mark()
    
    def type_mark(self) -> None:
        ''' <type_mark> ::=
                  integer | float | string | bool
                | <identifier>
                | enum {<identifier> ( , <identifier> )* }
        '''
        if self.print_bool: print("type mark")
        if checkToken("integer") or checkToken("float") or checkToken("string") 
                or checkToken("bool"):
            self.nextToken()
        elif checkToken("enum"):
            self.nextToken()
            self.matchToken("{")
            self.identifier()
            while self.checkToken(","):
                self.nextToken()
                self.identifier()
            self.matchToken("}")
        else:
            self.identifier()
    
    def bound(self) -> None:
        ''' <bound> ::=
                <number>
        '''
        if self.print_bool: print("bound")
        self.number()
    
    def statement(self) -> None:
        ''' <statement> ::=
                  <assignment_statement>
                | <if_statement>
                | <loop_statement>
                | <return_statement>
        '''
        if self.print_bool: print("statement")
        if self.checkToken("return"):
            self.return_statement()
        elif self.checkToken("for"):
            self.loop_statement()
        elif self.checkToken("if"):
            self.if_statement()
        else:
            self.assignment_statement()

    def procedure_call(self) -> None:
        ''' <procedure_call> ::=
                <identifier> ( [<argument_list>] )
        '''
        if self.print_bool: print("procedure call")
        self.identifier()
        self.matchToken("(")
        if not self.checkToken(")"):
            self.argument_list()
        self.matchToken(")")
    
    def assignment_statement(self) -> None:
        ''' <assignment_statement> ::=
                <destination> := <expression>
        '''
        if self.print_bool: print("assignment statement")
        self.destination()
        self.matchToken(":=")
        self.expression()
    
    def destination(self) -> None:
        ''' <destination> ::=
                <identifier> [[<expression>]]
        '''
        if self.print_bool: print("destination")
        self.identifier()
        if self.checkToken("["):
            self.nextToken()
            self.expression()
            self.checkToken("]")
    
    def if_statement(self) -> None:
        ''' <if_statement> ::=
                if (<expression>) then (<statement> ;)*
                [else ( <statement> ; )*]
                end if
        '''
        if self.print_bool: print("if")
        self.matchToken("if")
        self.matchToken("(")
        self.expression()
        self.matchToken(")")
        self.matchToken("then")
        self.matchToken("(")
        while self.checkToken(")"):
            self.statement()
            self.matchToken(";")
        self.nextToken()
        if self.checkToken("else"):
            self.nextToken()
            while self.checkToken(")"):
                self.statement()
                self.matchToken(";")
            self.nextToken()
        self.matchToken("end")
        self.matchToken("if")        

    def loop_statement(self) -> None:
        ''' <loop_statement> ::=
                for ( <assignment_statement> ; <expression> )
                    ( <statement> ;)*
                end for
        '''
        if self.print_bool: print("for")
        self.matchToken("for")
        self.matchToken("(")
        self.assignment_statement()
        self.matchToken(";")
        self.expression()
        self.(")")
        while not self.checkToken("end"):
            self.statement()
            self.matchToken(";")
        self.nextToken()
        self.matchToken("for")
    
    def return_statement(self) -> None:
        ''' <return_statement> ::=
                return <expression>
        '''
        if self.print_bool: print("return")
        self.matchToken("return")
        self.expression()

    def identifier(self) -> None:
        ''' <identifier> ::=
                [a-zA-Z] [a-zA-Z0-9_]*
        '''
        if self.print_bool: print("identifier")
        self.matchType("ID")

    def expression(self) -> None:
        ''' <expression> ::=
                  <expression> & <arithOp>
                | <expression> | <arithOp>
                | [not] <arithOp>
        '''
        if self.print_bool: print("expression")
        if self.checkPeek("&") or self.checkPeek("|"):
            self.expression()
            self.nextToken()
        elif self.checkToken("not"):
            self.nextToken()
        self.arithOp()

    def arithOp(self) -> None:
        ''' <arithOp> ::=
                  <arithOp> + <relation>
                | <arithOp> - <relation>
                | <relation>
        '''
        if self.print_bool: print("artih op")
        if self.checkPeek("+") or self.checkPeek("-"):
            self.arithOp()
            self.nextToken()
        self.relation()
    
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
        if self.print_bool: print("relation")
        if self.checkPeek('<') or self.checkPeek('>') or self.checkPeek('>=') or
                self.checkPeek('<=') or self.checkPeek(==) or self.checkPeek("!="):
            self.relation()
            self.nextToken()
        self.term()

    def term(self) -> None:
        ''' <term> ::=
                  <term> * <factor>
                | <term> / <factor>
                | <factor>
        '''
        if self.print_bool: print("term")
        if self.checkPeek("*") or self.checkPeek("/"):
            self.term()
            self.nextToken()
        self.factor()

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
        if self.print_bool: print("factor")
        if self.checkToken("("):
            self.nextToken()
            self.expression()
            self.match(")")
        elif self.checkType("ID"):
            if self.checkPeek("("):
                self.procedure_call()
            elif self.checkPeek("["):
                self.name()
            else:
                self.number()
        elif self.checkToken("-"):
            self.nextToken()
            if self.checkPeek("["):
                self.name()
            else:
                self.number()
        elif self.checkType("literal"):
            self.string()
        elif self.checkToken("false"):
            self.nextToken()        
        else:
            self.matchToken("true"):

    def name(self) -> None:
        ''' <name> ::=
                <identifier> [ [<expression>] ]
        '''
        if self.print_bool: print("name")
        self.identifier()
        self.matchToken("[")
        if not self.checkToken("]")
            self.expression()
        self.matchToken("]")

    def argument_list(self) -> None:
        ''' <argument_list> ::=
                  <expression> , <argument_list>
                | <expression>
        '''
        if self.print_bool: print("argument list")
        self.expression()
        if self.checkToken(","):
            self.nextToken()
            self.argument_list()
    
    def number(self) -> None:
        ''' <number> ::=
                [0-9][0-9_]*[.[0-9_]*]
        '''
        if self.print_bool: print("number")
        self.matchType("ID")

    def string(self) -> None:
        ''' <string> ::=
                "[^"]*"
        '''
        if self.print_bool: print("string")
        self.matchType("Literal")
    
    ''' End of Parsing Statements '''