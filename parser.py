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
    def __init__(self, filename, sprint_bool=False,print_bool=False, error_file='error_log.txt') -> None:
        self.s = Scanner(filename)
        self.current_token = Null()
        self.next_token = Null()
        self.print_bool = print_bool
        self.error_file = error_file
        self.sprint_bool = sprint_bool

        #while self.current_token == None:
        self.nextToken()
        self.nextToken()

    def nextToken(self) -> None:
        ''' Gets the next token for current and next self variables
        '''
        self.current_token = self.next_token
        if self.sprint_bool: print("TOKEN: ",self.current_token,self.current_token.kind)
        self.next_token = self.s.getToken()
        #while self.current_token.text != None:
        #    self.nextToken()
    
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
        if not self.checkToken(check_token):
            message = (f"{bcolors['FAIL']}ERROR: Unexpected token '{bcolors['BOLD']}{self.current_token}{bcolors['ENDC']}"
                    f"{bcolors['FAIL']}' on line number {bcolors['UNDERLINE']}{self.s.line_counter + 1}{bcolors['ENDC']}"
                    f"{bcolors['FAIL']}. '{check_token}' expected.{bcolors['ENDC']}")
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
                    f"{bcolors['FAIL']} on line number {bcolors['UNDERLINE']}{self.s.line_counter + 1}{bcolors['ENDC']}"
                    f"{bcolors['FAIL']}. type {check_token} expected.{bcolors['ENDC']}")
        self.nextToken()

    def parse(self):
        self.program()

    ########################################################################

    ''' Parsing Statements '''

    def program(self) -> None:
        ''' <program> ::= 
                <program_header><program_body> .
        '''
        if self.print_bool: print("program")
        # might not need to use a WHILE loop here
        while self.current_token.text != "EOF":
            self.program_header()
            self.program_body()

    def program_header(self) -> None:
        ''' <program_header> ::= 
                program <identifier> is
        '''
        if self.print_bool: print("program_header")
        self.matchToken("program")
        self.identifier()
        self.matchToken("is")

    def program_body(self) -> None:
        ''' <program_body> ::= 
                        ( <decleration> ; )*
                    begin
                        ( <statement> ; )*
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
        self.matchToken(".")
    
    def decleration(self) -> None:
        ''' <decleration> ::=
                  [global] <procedure_decleration>
                | [global] <variable_decleration> 
                | [global] <type_decleration>
        '''
        if self.print_bool: print("decleration")
        if self.checkToken("global"):
            if self.print_bool: print("global")
            self.nextToken()
        if self.checkToken("procedure"):
            self.procedure_decleration()
        elif self.checkToken("variable"):
            self.variable_decleration()
        else:
            self.type_decleration()
        
    def procedure_decleration(self) -> None:
        ''' <procedure_decleration> ::=
                <procedure_header><procedure_body>
        '''
        if self.print_bool: print("procedure decleration")
        self.procedure_header()
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
                    (<decleration> ;)*
                begin
                    (<statement> ;)*
                end procedure
        '''
        if self.print_bool: print("procedure body")
        while not self.checkToken("begin"):
            self.decleration()
            self.matchToken(";")
        self.nextToken()
        while not self.checkToken("end"):
            self.statement()
            self.matchToken(";")
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
            self.matchToken("]")
        
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
        if (self.checkToken("integer") or self.checkToken("float") or self.checkToken("string") or
                self.checkToken("bool")):
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
            self.matchToken("]")
    
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
        while not self.checkToken("else") and not self.checkToken("end"):
            self.statement()
            self.matchToken(";")
        if self.checkToken("else"):
            self.nextToken()
            while not self.checkToken("end"):
                self.statement()
                self.matchToken(";")
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
        self.matchToken(")")
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
        ''' **OLD GRAMMER**
            <expression> ::=
                  <expression> & <arithOp>
                | <expression> | <arithOp>
                | [not] <arithOp>
            
            **NEW GRAMMER**
            <expression> ::=
                [not] <arithOp> <expression_prime>
        '''
        if self.print_bool: print("expression")
        if self.checkToken("not"):
            self.nextToken()
        self.arithOp()
        self.expression_prime()
    
    def expression_prime(self) -> None:
        ''' <expression_prime> ::=
                  & [not] <arithOp> <expression_prime>
                | | [not] <arithOp> <expression_prime>
                | None
        '''
        if self.checkToken("&") or self.checkToken("|"):
            self.nextToken()
            if self.checkToken("not"):
                self.nextToken()
            self.arithOp()
            self.expression_prime()
        else:
            pass        

    def arithOp(self) -> None:
        ''' **OLD GRAMMER** 
            <arithOp> ::=
                  <arithOp> + <relation>
                | <arithOp> - <relation>
                | <relation>
            **NEW GRAMMER**
            <arithOp> ::=
                <relation> <arithOp_prime>
        '''
        if self.print_bool: print("artih op")
        self.relation()
        self.arithOp_prime()

    def arithOp_prime(self) -> None:
        ''' <arithOp_prime> ::=
                  + <relation> <arithOp_prime>
                | - <relation> <arithOp_prime>
                | None
        '''
        if self.checkToken("+") or self.checkToken("-"):
            self.nextToken()
            self.relation()
            self.arithOp_prime()
        else:
            pass
    
    def relation(self) -> None:
        ''' **OLD GRAMMER**
            <relation> ::=
                  <relation> < <term>
                | <relation> > <term>
                | <relation> >= <term>
                | <relation> <= <term>
                | <relation> == <term>
                | <relation> != <term>
                | <term>
        
            A = Aa | Ab | Ac | Ad | Ae | Af | y

            **NEW GRAMMER TO ELIM LR**
            A = yA'
            A' = aA' | bA' | cA' | dA' | eA' | fA' | /0

            <relation> ::= 
                <term> <relation_prime>

        '''
        if self.print_bool: print("relation")
        self.term()
        self.relation_prime()

    def relation_prime(self) -> None:
        ''' <relation_prime> ::=
                  < <term> <relation_prime> 
                | > <term> <relation_prime> 
                | >= <term> <relation_prime> 
                | <= <term> <relation_prime> 
                | == <term> <relation_prime> 
                | != <term> <relation_prime> 
                | None
        '''
        if (self.checkToken("<") or self.checkToken(">") or self.checkToken(">=") 
                or self.checkToken("<=") or self.checkToken("==") or self.checkToken("!=")):
            self.nextToken()
            self.term()
            self.relation_prime()
        else:
            pass

    def term(self) -> None:
        ''' **OLD GRAMMER**
            <term> ::=
                  <term> * <factor>
                | <term> / <factor>
                | <factor>
            
            **NEW GRAMMER**
            <term> ::=
                <factor> <term_prime>
        '''
        if self.print_bool: print("term")
        self.factor()
        self.term_prime()
    
    def term_prime(self) -> None:
        ''' <term_prime> ::=
                  * <factor> <term_prime>
                | / <factor> <term_prime>
                | None
        '''
        if self.checkToken("*") or self.checkToken("/"):
            self.nextToken()
            self.factor()
            self.term_prime()
        else:
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
        if self.print_bool: print("factor")
        
        if self.checkToken("("):
            self.nextToken()
            self.expression()
            self.matchToken(")")
        elif self.checkType("ID") or self.checkType("Keyword"):
            if self.checkPeek("("):
                self.procedure_call()
            # check for name
            elif self.current_token.text.isnumeric():
                self.number()
            else:
                self.name()
        elif self.checkToken("-"):
            self.nextToken()
            if self.current_token.text.isnumeric():
                self.number()
            else:
                self.name()
        elif self.checkType("Literal"):
            self.string()
        elif self.checkToken("false"):
            self.nextToken()        
        else:
            self.matchToken("true")

    def name(self) -> None:
        ''' <name> ::=
                <identifier> [ [<expression>] ]
        '''
        if self.print_bool: print("name")
        self.identifier()
        if self.checkToken("["):
            self.nextToken()
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