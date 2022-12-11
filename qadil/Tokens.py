import re

class TokenType:

    def __init__(self, name, rege=None):
        self.name = name
        if rege:
            self.rege = re.compile(rege)

class Token:

    SYMBOL = TokenType('SYMBOL', r'&')
    BEGINENV = TokenType('BEGINENV', r'\\begin\{([A-Za-z\*]+)\}')
    CONTROLSEQ = TokenType('CONTROLSEQ', r'\\(\\|,|\{|\}|#|%|&|[A-Za-z*]+| )') # Special: '\', ',',' '(csq blankspace)
    DISPLAYDELIMITER = TokenType('DISPLAYDELIMITER',  r'\$\$')
    ENDENV = TokenType('ENDENV', r'\\end\{([A-Za-z\*]+)\}')
    BEGINGROUP = TokenType('BEGINGROUP', r'\{')
    MATHDELIMITER = TokenType('MATHDELIMITER',  r'\$')
    NEWLINE = TokenType('NEWLINE', r'\n')
    PARAGRAPH = TokenType('PARAGRAPH', r'\n[ \t]*\n\s*') # One blank line = new paragraph
    PERCENT = TokenType('PERCENT', r'%.*[\n|$]')
    ENDGROUP = TokenType('ENDGROUP', r'\}')
    LEFTBRACKET = TokenType('LEFTBRACKET', r'\[')
    RIGHTBRACKET = TokenType('RIGHTBRACKET', r'\]')
    SPACE = TokenType('SPACE', r'[ \t]')
    WORD = TokenType('WORD', r'[^ \\\{\}\$\%&\n\[\]]+') # Take care of dangling '#' later
    TEXT = TokenType('TEXT')
    
    # Ordering important below! E.g. DISPLAYDELIMITER must come before MATHDELIMITER
    
    tokenids = (
    PARAGRAPH,
    NEWLINE,
    SPACE,
    SYMBOL,
    BEGINENV,
    ENDENV,
    CONTROLSEQ,
    BEGINGROUP,
    ENDGROUP,
    LEFTBRACKET,
    RIGHTBRACKET,    
    DISPLAYDELIMITER,
    MATHDELIMITER,
    WORD,
    PERCENT,
    TEXT    
    )

    def __init__(self, type, content):
        self.type = type
        self.content = content

    def __str__(self):
        return "<{type}, {content}>".format(type=self.type.name, content=self.content)

