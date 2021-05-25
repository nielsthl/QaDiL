import re
import io

# Definition and expansion of macros must be handled in tokenize

class Macros:

    def __init__(self):
        self.macros = {}

    def iscs(self, name):
        if self.tok == "CONTROLSEQ":
            if self.value == name:
                return True
        return False

    def ismacro(self):
       if self.tok == "CONTROLSEQ":
           return self.value in self.macros.keys()
       return False
 
    def swallowLBracket(self):
       self.getnexttok()
       if self.tok != "BEGINGROUP":
           lineno = self.countlines(self.pos) 
           raise Exception("Missing {")

    
    def parseBalancedbrackets(self):
        self.swallowLBracket()
        parcount = 1
        innerst = ""
        while True:
            self.getnexttok()
            if self.endofinput:
                raise Exception("Missing terminating } at line " + str(self.countlines(self.pos)))
            if self.tok == "BEGINGROUP":
                innerst += self.value
                parcount += 1
                continue
            if self.tok == "ENDGROUP":
                parcount -= 1
                if (parcount == 0):
                    break
            innerst += self.value

        return innerst

    def includefile(self):

        regex = r'\{(.*?)\}'
        regc = re.compile(regex)
        match = regc.match(self.inputstring, self.pos)

        if match:
            filename = match.group(1)
            self.pos = match.end(0)
        else:
            lineno = self.countlines(self.pos)
            raise Exception("Error in include control sequence")

        filein = io.open(filename, "r", encoding="utf8")
        returnstr = filein.read()
        filein.close()

        self.inputstring = returnstr + self.inputstring[self.pos:] # Insert text from file
        self.pos = 0


    
    def storemacro(self):
        #
        # Encountered \newcommand{\name}[1]{.. def ..}
        #
        # Swallow and store def of \name
        #

        regex = r'\{(.*?)\}'
        regc = re.compile(regex)
        match = regc.match(self.inputstring, self.pos)
        if match:
            macro = match.group(1)
            self.pos = match.end(0)
        else:
            lineno = self.countlines(self.pos)
            raise Exception("Error in newcommand control sequence")


        if macro:
            if (macro[0] != '\\'):
                raise Exception("Macro name must begin with \\")
            #macro = macro[1:]
        else:
            raise Exception("Empty macro")

        # Parse [noofargs]

        regex = r'\[(.*?)\]'
        regc = re.compile(regex)
        match = regc.match(self.inputstring, self.pos)
        if match:
            noofargs = int(match.group(1))
            self.pos = match.end(0)
        else:
            noofargs = 0

        # For {substtkt} we cannot match using regex. We need to simulate a stack for pairs of { and }:

        subst = self.parseBalancedbrackets()

        self.macros[macro] = (noofargs, subst)

        
    def expandmacro(self):

        macroname = self.value
        (noofargs, subst) = self.macros[macroname]
        
        # Pick out parameters in \macroname{par1}...{parN}
        
        args = []
        for i in range(noofargs):
            args.append(self.parseBalancedbrackets())

        # Substitute #1->par1, ..., #N -> parN
        
        for idx, val in enumerate(args):
            subst = subst.replace('#'+str(idx+1), val)

            '''
        self.inputstring = self.inputstring[:uptoposition] + subst + self.inputstring[self.pos:]
        self.pos = uptoposition
            '''
            
        self.inputstring = subst + self.inputstring[self.pos:]
        self.pos = 0
