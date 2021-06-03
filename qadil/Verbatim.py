import re
import io
from Tokens import Token, TokenType

# Handling of verbatim environments

class Verbatim:

    def handlecode(self):

        regex = r'(.*?)\\end\{code\}'
        regc = re.compile(regex, re.DOTALL)
        match = regc.match(self.inputstring, self.pos)

        if match:
            txt = match.group(1)
            self.pos = match.end(0)
            # Escape '<' and '>'
            txt = txt.replace("<", "&lt;").replace(">", "&gt;")
            self.tokenlist.append(Token(TokenType("BEGINENV"), "\\begin{code}"))
            self.tokenlist.append(Token(TokenType("TEXT"), txt))
            self.tokenlist.append(Token(TokenType("ENDENV"), "\\end{code}"))
        else:
            lineno = self.countlines(self.pos)
            raise Exception("Code environment not ended properly")

    def handlehtml(self):

        regex = r'(.*?)\\end\{html\}'
        regc = re.compile(regex, re.DOTALL)
        match = regc.match(self.inputstring, self.pos)

        if match:
            txt = match.group(1)
            self.pos = match.end(0)
            self.tokenlist.append(Token(TokenType("TEXT"), txt))
        else:
            lineno = self.countlines(self.pos)
            raise Exception("Html environment not ended properly")

        
    def handleverbatim(self):
        
        regex = r'(.*?)\\end\{verbatim\}'
        regc = re.compile(regex, re.DOTALL)
        match = regc.match(self.inputstring, self.pos)

        if match:
            txt = match.group(1)
            self.pos = match.end(0)
            self.tokenlist.append(Token(TokenType("BEGINENV"), "\\begin{verbatim}"))
            self.tokenlist.append(Token(TokenType("TEXT"), txt))
            self.tokenlist.append(Token(TokenType("ENDENV"), "\\end{verbatim}"))
        else:
            lineno = self.countlines(self.pos)
            raise Exception("Verbatim environment not ended properly")
