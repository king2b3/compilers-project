""" Holds the parser structure for the language.

    Created on: 1-29-2021
    Version: Python 3.8.5
    Created by: Bayley King (https://github.com/king2b3)
"""

# file imports
from compiler import Compiler
from scanner import Scanner
from tokens import *
from global_params import *
from symbol import SymbolTable
from codegen import CodeGen
from typecheck import *

class Parser(Compiler):
    """ Class for the parser. Contains methods needed for parse, and calls the scanner. """    
    def __init__(self, filename, sprint_bool=False,print_bool=False, error_file='error_log.txt', print_table=False) -> None:
        # inits of other classes
        self.s = Scanner(filename)
        self.t = SymbolTable()
        self.c = CodeGen(filename)
        self.tc = TypeCheck()
        # bool to hold if we are in the global space
        self.level = 0
        # variable declerations
        self.print_bool = print_bool
        self.error_file = error_file
        self.sprint_bool = sprint_bool
        self.print_table = print_table
        # populates the first current and next tokens from the scanner
        self.current_token = Null()
        self.next_token = Null()
        self.third_token = Null()
        self.nextToken()
        self.nextToken()
        self.nextToken()

    def nextToken(self) -> None:
        """ Gets the next token for current and next self variables """
        self.current_token = self.next_token
        if self.sprint_bool: print(f"\tCurrent Token {self.current_token.text}\t\tToken Kind{self.current_token.kind}")
        self.next_token = self.third_token
        self.third_token = self.s.getToken()

    def checkToken(self, check_token) -> bool:
        """ Checks if the current token is the same as the expected token """
        return check_token == self.current_token.text

    def checkPeek(self, check_token) -> bool:
        """ Checks if the next token is the same as the expected token """
        return check_token == self.next_token.text

    def matchToken(self, check_token) -> bool:
        """ Checks if the current token matches the expected token. 
            Throws error if match fails 
        """
        if not self.checkToken(check_token):
            message = (f"{bcolors['FAIL']}ERROR: Unexpected token '{bcolors['BOLD']}{self.current_token}{bcolors['ENDC']}"
                    f"{bcolors['FAIL']}' on line number {bcolors['UNDERLINE']}{self.s.line_counter + 1}{bcolors['ENDC']}"
                    f"{bcolors['FAIL']}. '{check_token}' expected.{bcolors['ENDC']}")
            self.reportError(message)
        self.nextToken()
    
    def checkType(self, check_token) -> bool:
        """ Checks if the current token type matches the expected type """
        return check_token == self.current_token.kind

    def matchType(self, check_token) -> bool:
        """ Checks if the token type is the expected type
            Throws error if matchToken fails
        """
        if not self.checkType(check_token):
            message = (f"{bcolors['FAIL']}ERROR: Unexpected type {bcolors['BOLD']}{self.current_token.kind}{bcolors['ENDC']}"
                    f"{bcolors['FAIL']} on line number {bcolors['UNDERLINE']}{self.s.line_counter + 1}{bcolors['ENDC']}"
                    f"{bcolors['FAIL']}. type {check_token} expected.{bcolors['ENDC']}")
            self.reportError(message)
        self.nextToken()

    def redefinedError(self) -> None:
        """ Error message when variable is re-defined in a scope. """
        message = (f"{bcolors['FAIL']}ERROR: Re-declared variable {bcolors['BOLD']}{self.current_token.text}{bcolors['ENDC']}"
                f"{bcolors['FAIL']} on line number {bcolors['UNDERLINE']}{self.s.line_counter + 1}{bcolors['ENDC']}")
        self.reportError(message)

    def undefinedError(self, name) -> None:
        """ Error message when variable is undefined in a scope. """
        message = (f"{bcolors['FAIL']}ERROR: Undeclared variable {bcolors['BOLD']}{name}{bcolors['ENDC']}"
                f"{bcolors['FAIL']} on line number {bcolors['UNDERLINE']}{self.s.line_counter + 1}{bcolors['ENDC']}")
        self.reportError(message)

    def typeError(self, name1, name2) -> None:
        """ Error message when there is a type mismatch. """
        message = (f"{bcolors['FAIL']}ERROR: Type mistmatch {bcolors['BOLD']}{name1}{bcolors['ENDC']}"
                f"{bcolors['FAIL']} and {bcolors['BOLD']}{name2}{bcolors['ENDC']}"
                f"{bcolors['FAIL']} on line number {bcolors['UNDERLINE']}{self.s.line_counter + 1}{bcolors['ENDC']}")
        self.reportError(message)

    def symbolTableAdd(self, name=None, symbol=None, layer=None) -> None:
        """ Adds a symbol to the symbol table, across either scope. """
        # allows for passed params or taken from class variables
        if layer == None:
            layer = self.level
        if not name:
            name = self.current_token.text
        if not symbol:
            symbol = self.next_token

        if not self.t.insert(name, symbol, layer):
            self.redefinedError()
        if self.print_table: print(self.t)
    
    def type_check(self, name1, name2) -> None:
        """ Checks the type of two variables from the table """
        if self.print_table: print(self.t)
        
        if name1 == "(":
            name1 = self.next_token.text
            name2 = self.third_token.text
        if name2 == "(":
            name2 = self.third_token.text

        if (type1 := self.t.lookup(name1)) == None:
            self.undefinedError(name1)
        if name2[0] == '"':
            # type check for string literals
            type2 = name2
        elif (type2 := self.t.lookup(name2)) == None and \
                self.id_type(name2) == "symbol" :
            self.undefinedError(name2)
        # calls the type check method
        self.tc.type_check(type1, type2)
    
    def hard_check(self, name1, name2) -> None:
        """ Hard check on procedure type checking """
        if (type1 := t.lookup(name1)) == None:
            self.undefinedError(name1)
        if (type2 := t.lookup(name2)) == None:
            self.undefinedError(name2)
        # calls the type check method
        tc.hard_check(type1, type2)

    def id_type(self, val) -> str:
        if (temp := checknum(val)):
            if temp == "symbol":
                return val
            else:
                return temp
        else:
            # sanity check error, shouldn't reach here in the code path
            self.undefinedError(val)
    
    def parse(self):
        self.c.write_line("void main(){\n")
        self.program()
        self.c.write_line("}")

    ########################################################################

    """ Parsing Statements """

    def program(self) -> None:
        """ <program> ::= 
                <program_header><program_body> .
        """
        if self.print_bool: print("program")
        # might not need to use a WHILE loop here
        while self.current_token.text != "EOF":
            self.program_header()
            self.program_body()

    def program_header(self) -> None:
        """ <program_header> ::= 
                program <identifier> is
        """
        if self.print_bool: print("program_header")
        self.matchToken("program")
        self.identifier()
        self.matchToken("is")

    def program_body(self) -> None:
        """ <program_body> ::= 
                        ( <decleration> ; )*
                    begin
                        ( <statement> ; )*
                    end program
        """
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
        """ <decleration> ::=
                  [global] <procedure_decleration>
                | [global] <variable_decleration> 
        """
        if self.print_bool: print("decleration")
        if self.checkToken("global"):
            if self.print_bool: print("global")
            self.nextToken()
            # global add
            if self.print_bool: print(f"\nGlobal variable added\n")
            self.level = 0
        if self.checkToken("procedure"):
            self.procedure_decleration()
        elif self.checkToken("variable"):
            self.variable_decleration()
        
    def procedure_decleration(self) -> None:
        """ <procedure_decleration> ::=
                <procedure_header><procedure_body>
        """
        if self.print_bool: print("procedure decleration")
        # add local table from stack
        if self.print_table: print(self.t)
        self.t.append_stack()
        if self.print_table: print(f"STACK APPENDED\n")
        if self.print_table: print(self.t)
        self.procedure_header()
        self.procedure_body()
        # remove local table from stack
        if self.print_table: print(self.t)
        self.t.pop_stack()
        if self.print_table: print(f"\nSTACK POPPED\n")
        if self.print_table: print(self.t)
        if len(self.t.local_table) == 0:
            self.level = 0

    def procedure_header(self) -> None:
        """ <procedure_header> ::=
                procedure <identifier> : <type_mark> ( [<parameter_list>] )
        """
        if self.print_bool: print("procedure header")
        self.matchToken("procedure")

        
        if self.level == 1:
            self.t.local_table[-2].insert(self.current_token.text,"procedure")
        else:
            self.symbolTableAdd(symbol="procedure")
        self.level = 1
        self.symbolTableAdd(symbol="procedure")

        self.identifier()
        self.matchToken(":")
        self.type_mark()
        self.matchToken("(")
        if not self.checkToken(")"):
            self.parameter_list()
        self.matchToken(")")
    
    def parameter_list(self) -> None:
        """ <parameter_list> ::=
                  <parameter> , <parameter_list>
                | <parameter>
        """
        if self.print_bool: print("parameter list")
        self.parameter()
        if self.checkToken(","):
           self.nextToken()
           self.parameter_list()            

    def parameter(self) -> None:
        """ <parameter> ::=
                <variable_decleration>
        """
        if self.print_bool: print("parameter")
        self.variable_decleration()
    
    def procedure_body(self) -> None:
        """ <procedure_body> ::=
                    (<decleration> ;)*
                begin
                    (<statement> ;)*
                end procedure
        """
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
        """ <variable_decleration> ::=
                variable <identifier> : <type_mark> [[<bound>]]
        """
        if self.print_bool: print("variable decleration")
        
        self.matchToken("variable")
        temp_name = self.current_token.text
        self.identifier()
        self.matchToken(":")
        temp_val = self.current_token.text
        self.symbolTableAdd(name=temp_name,symbol=temp_val)
        self.type_mark()
        if self.checkToken("["):
            self.nextToken()
            self.bound()
            self.matchToken("]")
    
    def type_mark(self) -> None:
        """ <type_mark> ::=
                  integer | float | string | bool
        """
        if self.print_bool: print("type mark")
        if (self.checkToken("integer") or self.checkToken("float") or self.checkToken("string") or
                self.checkToken("bool")):
            self.nextToken()
        else:
            self.typeError(self.current_token.text, "integer, float, string, or bool")
    
    def bound(self) -> None:
        """ <bound> ::=
                <number>
        """
        if self.print_bool: print("bound")
        self.number()
    
    def statement(self) -> None:
        """ <statement> ::=
                  <assignment_statement>
                | <if_statement>
                | <loop_statement>
                | <return_statement>
        """
        #### NEED TO RETURN TYPE ####
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
        """ <procedure_call> ::=
                <identifier> ( [<argument_list>] )
        """
        if self.print_bool: print("procedure call")

        self.identifier()
        self.matchToken("(")
        if not self.checkToken(")"):
            self.argument_list()
        self.matchToken(")")
    
    def assignment_statement(self) -> None:
        """ <assignment_statement> ::=
                <destination> := <expression>
        """
        #### NEED TO RETURN TYPE ####
        if self.print_bool: print("assignment statement")
        # temp save of token for type checking
        var1 = self.current_token.text
        self.destination()
        self.matchToken(":=")
        
        # put checks in calls? Or use returns?
        var2 = self.current_token.text
        if var2 == "-":
            self.nextToken()
            var2 = self.current_token.text
            self.c.write_line("- ")
        
        self.expression()
        self.type_check(var1, var2)

    def destination(self) -> None:
        """ <destination> ::=
                <identifier> [[<expression>]]
        """
        if self.print_bool: print("destination")
        self.identifier()
        if self.checkToken("["):
            self.nextToken()
            self.expression()
            self.matchToken("]")
    
    def if_statement(self) -> None:
        """ <if_statement> ::=
                if (<expression>) then (<statement> ;)*
                [else ( <statement> ; )*]
                end if
        """
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
        """ <loop_statement> ::=
                for ( <assignment_statement> ; <expression> )
                    ( <statement> ;)*
                end for
        """
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
        """ <return_statement> ::=
                return <expression>
        """
        #### NEED TO RETURN TYPE ####
        if self.print_bool: print("return")
        self.matchToken("return")
        self.expression()

    def identifier(self) -> None:
        """ <identifier> ::=
                [a-zA-Z] [a-zA-Z0-9_]*
        """
        if self.print_bool: print("identifier")
        if self.checkType("ID"):
            self.matchType("ID")
        else:
            self.matchType("Keyword")

    def expression(self) -> None:
        """ **OLD GRAMMER**
            <expression> ::=
                  <expression> & <arithOp>
                | <expression> | <arithOp>
                | [not] <arithOp>
            
            **NEW GRAMMER**
            <expression> ::=
                [not] <arithOp> <expression_prime>
        """
        #### NEED TO RETURN TYPE ####
        if self.print_bool: print("expression")
        if self.checkToken("not"):
            self.nextToken()
        self.arithOp()
        self.expression_prime()
    
    def expression_prime(self) -> None:
        """ <expression_prime> ::=
                  & [not] <arithOp> <expression_prime>
                | | [not] <arithOp> <expression_prime>
                | None
        """
        if self.checkToken("&") or self.checkToken("|"):
            self.nextToken()
            if self.checkToken("not"):
                self.nextToken()
            self.arithOp()
            self.expression_prime()
        else:
            pass        

    def arithOp(self) -> None:
        """ **OLD GRAMMER** 
            <arithOp> ::=
                  <arithOp> + <relation>
                | <arithOp> - <relation>
                | <relation>
            **NEW GRAMMER**
            <arithOp> ::=
                <relation> <arithOp_prime>
        """
        #### NEED TO RETURN TYPE ####
        if self.print_bool: print("artih op")
        self.relation()
        self.arithOp_prime()

    def arithOp_prime(self) -> None:
        """ <arithOp_prime> ::=
                  + <relation> <arithOp_prime>
                | - <relation> <arithOp_prime>
                | None
        """
        if self.checkToken("+") or self.checkToken("-"):
            self.nextToken()
            self.relation()
            self.arithOp_prime()
        else:
            pass
    
    def relation(self) -> None:
        """ **OLD GRAMMER**
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

        """
        #### NEED TO RETURN TYPE ####
        if self.print_bool: print("relation")
        self.term()
        self.relation_prime()

    def relation_prime(self) -> None:
        """ <relation_prime> ::=
                  < <term> <relation_prime> 
                | > <term> <relation_prime> 
                | >= <term> <relation_prime> 
                | <= <term> <relation_prime> 
                | == <term> <relation_prime> 
                | != <term> <relation_prime> 
                | None
        """
        if (self.checkToken("<") or self.checkToken(">") or self.checkToken(">=") 
                or self.checkToken("<=") or self.checkToken("==") or self.checkToken("!=")):
            self.nextToken()
            self.term()
            self.relation_prime()
        else:
            pass

    def term(self) -> None:
        """ **OLD GRAMMER**
            <term> ::=
                  <term> * <factor>
                | <term> / <factor>
                | <factor>
            
            **NEW GRAMMER**
            <term> ::=
                <factor> <term_prime>
        """
        #### NEED TO RETURN TYPE ####
        if self.print_bool: print("term")
        self.factor()
        self.term_prime()
    
    def term_prime(self) -> None:
        """ <term_prime> ::=
                  * <factor> <term_prime>
                | / <factor> <term_prime>
                | None
        """
        if self.checkToken("*") or self.checkToken("/"):
            self.nextToken()
            self.factor()
            self.term_prime()
        else:
            pass

    def factor(self) -> None:
        """ <factor> ::=
                  (<expression>)
                | <procedure_call>
                | [-] <name>
                | [-] <number>
                | <string>
                | true
                | false
        """
        #### NEED TO RETURN TYPE ####
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
        """ <name> ::=
                <identifier> [ [<expression>] ]
        """
        #### NEED TO RETURN TYPE ####
        if self.print_bool: print("name")
        self.identifier()
        if self.checkToken("["):
            self.nextToken()
            self.expression()
            self.matchToken("]")

    def argument_list(self) -> None:
        """ <argument_list> ::=
                  <expression> , <argument_list>
                | <expression>
        """
        if self.print_bool: print("argument list")
        self.expression()
        if self.checkToken(","):
            self.nextToken()
            self.argument_list()
    
    def number(self) -> None:
        """ <number> ::=
                [0-9][0-9_]*[.[0-9_]*]
        """
        if self.print_bool: print("number")
        self.matchType("ID")

    def string(self) -> None:
        """ <string> ::=
                "[^"]*"
        """
        if self.print_bool: print("string")
        self.matchType("Literal")
    
    """ End of Parsing Statements """