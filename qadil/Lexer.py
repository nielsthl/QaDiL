import re, sys
from Macros import Macros
from Verbatim import Verbatim
from Tokens import Token, TokenType

class LexerException(Exception):

    def __init__(self, msg, pos):
        self.msg = msg
        self.pos = pos

    def __str__(self):
        return "Error at position: {pos} - {msg}". format(pos = self.pos, msg = self.msg)

class Lexer(Macros, Verbatim):

    def __init__(self, inputstring):
        Macros.__init__(self)
        self.inputstring = inputstring
        self.pos = 0
        self.tok = None
        self.value = None
        self.curtok = None
        self.endofinput = False
        self.tokenlist = []
        self.tokenize()
        self.tokens = iter(self.tokenlist)

    def countlines(self, pos):
        return self.inputstring[:pos].count("\n") + 1


    def getnexttoken(self):
        self.endofinput = False
        try:
            tok = next(self.tokens)
            self.tok = tok.type.name
            self.value = tok.content
        except StopIteration:
            self.endofinput = True
     
    def getnexttok(self):
        if self.pos >= len(self.inputstring):
            self.endofinput = True
            return

        for tok in Token.tokenids:
            match = tok.rege.match(self.inputstring, self.pos)
            if match:
                self.tok = tok.name
                self.value = match.group(0)
                self.curtok = Token(tok, self.value)
                self.pos = match.end(0)
                return

        lineno = self.countlines(self.pos)    
        raise LexerException("Unknown token:"+self.inputstring[self.pos: self.pos+10], lineno)

    #
    # Functions at tokenize level:
    #
    # \newcommand, \include{filename}
    #
    # \macros
    #
    # \bye
    #
    # \begin{code}, \begin{verbatim}, \begin{html}
    #
        
    def tokenize(self):
        self.getnexttok()
        while not self.endofinput:

            if self.iscs("\\newcommand"):
                self.storemacro()
                self.getnexttok()
                continue

            if self.ismacro():
                self.expandmacro()
                self.getnexttok()
                continue

            if self.iscs("\\include"):
                self.includefile()
                self.getnexttok()
                continue
            
            if self.iscs("\\bye"): 
                self.endofinput = True
                continue

            # Stunts for handling code/verbatim/html environments.
            
            if self.tok == "BEGINENV":
                if self.value == "\\begin{code}":
                    self.handlecode()
                    self.getnexttok()
                if self.value == "\\begin{sage}":
                    self.handlesage()
                    self.getnexttok()
                if self.value == "\\begin{verbatim}":
                    self.handleverbatim()
                    self.getnexttok()
                if self.value == "\\begin{html}":
                    self.handlehtml()
                    self.getnexttok()
                if self.value == "\\begin{tikzpicture}":
                    self.handletikzpicture()
                    self.getnexttok()
                
                    

            self.tokenlist.append(self.curtok)
            self.getnexttok()
