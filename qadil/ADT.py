'''
Phrased in algebraic data types (Haskell) 
the structure of the AST is:


LaTeXList = [LaTeX]

LaTeX = 
Environment [LaTeXList] [LaTeXList] LaTeXList |
ControlSequence [LaTeXList] [LaTeXList] |
DisplayMath LaTeXList |
InlineMath LaTeXList |
* Parameter Int |
* Word String |
* Symbol |
* Comment String |
* Space |
* Paragraph
* NewLine |
* BeginGroup |
* EndGroup |
* LeftBracket |
* RightBRacket |

The classes marked by * are leaves in the AST.
'''

Types = [
    "LaTeXList",
    "ControlSequence",
    "Environment",
    "Symbol",
    "Word",
    "BeginGroup",
    "EndGroup",
    "LeftBracket",
    "RightBracket",
    "DisplayMath",
    "InlineMath",
    "Paragraph",
    "NewLine",
    "Space",
    "Text", # Arbitrary string without lexing
    "Comment",
    "Parameter"
    ]


class LaTeXList:
    def __init__(self):
        self.children = []

    def append(self, obj):
        self.children.append(obj)

    def __iter__(self):
        self.n= 0
        return self

    def __next__(self):
        if self.n < len(self.children):
            val = self.children[self.n]
            self.n += 1
            return val
        else:
            raise StopIteration
        
    def __len__(self):
        return len(self.children)
        
    def __getitem__(self, i):
        return self.children[i]

    def __setitem__(self, i, val):
        self.children[i] = val
    
    def __str__(self):
        s = "LaTeXList ["
        for c in self.children:
            s += c.__str__() +", "
        if len(self.children) > 0:
            s = s[:-2]
        s += "]"
        return s

class ControlSequence:
    def __init__(self, name):
        self.name = name
        self.args = [] # List of LaTeXList (arguments)
        self.opts = [] # List of LaTeXList (optional arguments)

    def __str__(self):
        s = "(ControlSequence: " + self.name + ", args: ["
        ret = ""
        for o in self.args:
            ret += o.__str__() + ", "
        if len(self.args) > 0:
            ret = ret[:-2]
        s += ret + "], opts: ["
        ret = ""
        for o in self.opts:
            ret += o.__str__() + ", "
        if len(self.opts) > 0:
            ret = ret[:-2]
        s += ret + "])"
        
        return s

class Environment:
    def __init__(self, name):
        self.name = name
        self.args = [] # List of LaTeXList (arguments)
        self.opts = [] # List of LaTeXList (optional arguments)
        self.body = LaTeXList()
        
    def __str__(self):
        s = "(Environment: " + self.name + ", args: ["
        ret = ""
        for o in self.args:
            ret += o.__str__() + ", "
        if len(self.args) > 0:
            ret = ret[:-2]
        s += ret + "], opts: ["
        ret = ""
        for o in self.opts:
            ret += o.__str__() + ", "
        if len(self.opts) > 0:
            ret = ret[:-2]
        s += ret + "] "
        s += self.body.__str__() + ")"
        
        return s

class InlineMath:
    def __init__(self):
        self.body = LaTeXList()

    def append(self, obj):
        self.body.append(obj)
        
    def __str__(self):
        return "InlineMath: " + self.body.__str__()

class DisplayMath:
    def __init__(self):
        self.body = LaTeXList()

    def append(self, obj):
        self.body.append(obj)
        
    def __str__(self):
        return "DisplayMath: " + self.body.__str__()

##### Leaves in AST below


class Word:
    def __init__(self, content):
        self.content = content 

    def __str__(self):
        return f'Word: "{self.content}"'

class Parameter:
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return f"Parameter: {self.content}"

class Symbol:
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return "SpecialCharacter: " + self.content

class BeginGroup:
    def __str__(self):
        return "BeginGroup"


class EndGroup:
    def __str__(self):
        return "EndGroup"

class LeftBracket:
    def __str__(self):
        return "LeftBracket"

class RightBracket:
    def __str__(self):
        return "rightBracket"

class Paragraph:
    def __str__(self):
        return "Paragraph"

class NewLine:
    def __str__(self):
        return "NewLine"

class Space:
    def __str__(self):
        return "Space"

class Text:
    def __init__(self, content):
        self.content = content 

    def __str__(self):
        return f'Text: "{self.content}"'

class Comment:
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return f"Comment: {self.content}"
