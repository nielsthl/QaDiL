from Parser import Parser
from ADT import Types
import sys

class Writer(Parser):
    
    def __init__(self, inputstring):
        Parser.__init__(self, inputstring)
        self.ltxaction = {}

        for t in Types:
            self.ltxaction[t] = getattr(self, t)
        
    def inspecthalt(self, txt, *args): # Debugging
        print(txt)
        for v in args:
            print(v)
        sys.exit(0)

    def inspectcont(self, txt, *args): # Debugging
        print(txt)
        for v in args:
            print(v)
        print('***\n')
        
    def typename(self, c):
        return type(c).__name__


    def nextskipblank(self, bc):
        c = bc
        while self.typename(c) in ["Space", "NewLine"]:
            c = next(bc)
        return c
    
    def parsechildren(self, obj):
        ostr = ""
#        print("In parsechildren, typename = ", self.typename(obj))
        for c in obj:
            ostr += self.ltxaction[self.typename(c)](c)
        return ostr

    def parsearg(self, obj, i):
        ostr = ""
        for c in obj.args[i]:
            ostr += self.ltxaction[self.typename(c)](c)
        return ostr

    def parseopt(self, obj, i):
        ostr = ""
        for c in obj.opts[i]:
            ostr += self.ltxaction[self.typename(c)](c)
        return ostr
    
#########################
    
    def LaTeXList(self, obj):
        return self.parsechildren(obj)
                    
    def Symbol(self, obj):
        return obj.content

    def Parameter(self, obj):
        return f"#{str(obj.content)}"
    
    def Word(self, obj):
        return obj.content

    def Environment(self, obj):
        try:
            return self.functions[obj.name](obj)
        except KeyError:
            value = "\\begin{" + obj.name + "}"
            args = ""
            for o in obj.args:
                ret = ""
                for c in o:
                    ret += self.ltxaction[self.typename(c)](c)
                args += '{' + ret + '}'
            opts = ""
            for o in obj.opts:
                ret = ""
                for c in o:
                    ret += self.ltxaction[self.typename(c)](c)
                opts += '[' + ret + ']'
                
            return  value + opts + args + self.parsechildren(obj.body) + "\\end{" + obj.name + "}"

    def ControlSequence(self, obj):

        try:
            return self.functions[obj.name](obj)
        except KeyError:
            value = "\\" + obj.name
            args = ""
            for o in obj.args:
                ret = ""
                for c in o:
                    ret += self.ltxaction[self.typename(c)](c)
                args += '{' + ret + '}'
            opts = ""
            for o in obj.opts:
                ret = ""
                for c in o:
                    ret += self.ltxaction[self.typename(c)](c)
                opts += '[' + ret + ']'
            #
            # The code below failed for the n-th root in KaTeX i.e., \sqrt[n]{2}
            # ret = value + args + opts

            # 18/10/20:
            # But if we do this, then \mathbb{R}[x] will fail as the polynomial ring!!
            # Terrible solution below!

            if value == "\\mathbb":
                ret = value + args + opts
            else:
                ret = value + opts + args

            return ret
        
    def BeginGroup(self, obj):
        return "{"

    def EndGroup(self, obj):
        return "}"

    def LeftBracket(self, obj):
        return "["

    def RightBracket(self, obj):
        return "]"
    
    def DisplayMath(self, obj):
        return self.displaymath(obj.body)

    def InlineMath(self, obj):
        return self.inlinemath(obj.body)
        
    def Paragraph(self, obj):
        return self.paragraph()
    
    def NewLine(self, obj):
        return "\n"
        
    def Space(self, obj):
        return " "

    def Text(self, obj):
        return obj.content
    
    def Comment(self, obj):
        if self.verbatim:
            return obj.content
        else:
            return ""
