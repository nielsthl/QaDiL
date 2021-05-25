from ADT import \
(LaTeXList, ControlSequence, Environment, Word,
 InlineMath, DisplayMath, Symbol, BeginGroup, EndGroup,
 LeftBracket, RightBracket, Space, NewLine, Comment, Text, Parameter, Paragraph)

import re
from Lexer import Lexer

from Tokens import Token

class ParserException(Exception):

    def __init__(self, msg, pos):
        self.msg = msg
        self.pos = pos

    def __str__(self):
        return "Error at line: {pos} - {msg}".format(pos = self.pos, msg = self.msg)

class Parser(Lexer):
    
    def __init__(self, inputstring):
        Lexer.__init__(self, inputstring)
        self.obj = LaTeXList()

        self.action = {}
        self.line = 1
        for tok in Token.tokenids:
            self.action[tok.name] = getattr(self, tok.name)

    def translate(self):
        
        self.getnexttoken()
        while(not self.endofinput):
            self.obj.children.append(self.action[self.tok]())

    
    def SYMBOL(self):

        value = self.value
        self.getnexttoken()
        return Symbol(value)

    def PARAMETER(self):
        value = self.value
        self.getnexttoken()
        return Parameter(int(value[1:])) # value = #123 -> value[1:] = 123
    
    def WORD(self):

        value = self.value
        self.getnexttoken()
        return Word(value)

    def BEGINENV(self):

        '''
        Encountered \begin{<name>}
        '''

        
        strmatch = self.value
        name = Token.BEGINENV.rege.match(strmatch).group(1)

        obj = Environment(name) 

        '''
        Parse arguments to environment:
        \begin{env}[o1]{a1}{a2}[o2]{a3}
        ...
        \end{env}

        parses into

        args = [a1, a2, a3]
        opts = [o1, o2]
        '''

        self.getnexttoken()
        while True:
            if (self.tok == "BEGINGROUP"): # argument
                self.getnexttoken()
                arg = LaTeXList()
                while (self.tok != "ENDGROUP" and not self.endofinput):
                    arg.append(self.action[self.tok]())
                obj.args.append(arg)
                self.getnexttoken()
            else:
                if (self.tok == "LEFTBRACKET"): # optional argument
                    self.getnexttoken()
                    arg = LaTeXList()
                    while (self.tok != "RIGHTBRACKET" and not self.endofinput):
                        arg.append(self.action[self.tok]())
                    obj.opts.append(arg)
                    self.getnexttoken()
                else:
                    break
                            
        while (self.tok != "ENDENV" and not self.endofinput):
            obj.body.append(self.action[self.tok]())
                        
        if (self.endofinput):
            raise ParserException("Premature end of file. Missing end of environment: " + name, self.line)
                
        if (self.ENDENV() != name):
            raise ParserException("Environment: " + name + " not ended correctly", self.line)

        self.getnexttoken()
        return obj

    def ENDENV(self):
        strmatch = self.value
        return Token.ENDENV.rege.match(strmatch).group(1)
        
    def CONTROLSEQ(self):

        '''
        Encountered \<csname> (control sequence)
        '''
        
        strmatch = self.value
        csname = Token.CONTROLSEQ.rege.match(strmatch).group(1)

        obj = ControlSequence(csname)

        '''
        Parse arguments here:

        \ct[o1]{a1}{a2}[o2]{a3}

        parses into

        args = [a1, a2, a3]
        opts = [o1, o2]
        '''

        self.getnexttoken()
        while True:
            if (self.tok == "BEGINGROUP"): # argument
                self.getnexttoken()
                arg = LaTeXList()
                while (self.tok != "ENDGROUP" and not self.endofinput):
                    arg.append(self.action[self.tok]())
                obj.args.append(arg)
                self.getnexttoken()
            else:
                if (self.tok == "LEFTBRACKET"): # optional argument
                    self.getnexttoken()
                    arg = LaTeXList()
                    while (self.tok != "RIGHTBRACKET" and not self.endofinput):
                        arg.append(self.action[self.tok]())
                    obj.opts.append(arg)
                    self.getnexttoken()
                else:
                    break
                    
        return obj
        
    def BEGINGROUP(self):
        self.getnexttoken()
        return BeginGroup()
        
    def ENDGROUP(self):
        self.getnexttoken()
        return EndGroup()

    def LEFTBRACKET(self):
        self.getnexttoken()
        return LeftBracket()

    def RIGHTBRACKET(self):
        self.getnexttoken()
        return RightBracket()

    def DISPLAYDELIMITER(self):

        #
        # Encountered $$...
        #

        obj = DisplayMath()

        self.getnexttoken()
        
        while (self.tok != "DISPLAYDELIMITER" and not self.endofinput):
            obj.body.append(self.action[self.tok]())
            
        if (self.endofinput):
            raise ParserException("Premature end of file. Missing $$.", self.line)

        self.getnexttoken()
        return obj

    def MATHDELIMITER(self):

        #
        # Encountered $...
        #

        obj = InlineMath()

        self.getnexttoken()
        
        while (self.tok != "MATHDELIMITER" and not self.endofinput):
            obj.body.append(self.action[self.tok]())
            
        if (self.endofinput):
            raise ParserException("Premature end of file. Missing $.", self.line)

        self.getnexttoken()
        return obj

    def PARAGRAPH(self):
        self.line += 2
        self.getnexttoken()
        return Paragraph()
    
    
    def PERCENT(self):
        value = self.value
        self.getnexttoken()
        return Comment(value)
        #
        # Forget about the rest of the line
        #
        # regex = r".*\n"
        regex = r".*(\n|$)" # Also handle comment before end of string
        
        regc = re.compile(regex)
        match = regc.match(self.inputstring, self.pos)

        if match:
            self.pos = match.end(0)
            self.getnexttoken()
        else:
            raise ParserException("Error in comment", self.line)
        return Comment()

    def TEXT(self):
        value = self.value
        self.getnexttoken()
        return Text(value)
        
    def NEWLINE(self):
        self.line += 1
        self.getnexttoken()
        return NewLine()

    def SPACE(self):
        self.getnexttoken()
        return Space()
        
        
