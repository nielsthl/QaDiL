# -*- coding: utf-8 -*

import io
import sys
import os
from PIL import Image


from Writer import Writer

class LaTeX(Writer):

    def emphasize(func):
    
        def emphfunc(self, obj):
            if len(obj.opts) > 0:
                content = self.parseopt(obj, 0)
                if content == "emph":
                    return f'\\begin{{tcolorbox}}{func(self, obj)}\\end{{tcolorbox}}'
            return func(self, obj)

        return emphfunc
    
    def __init__(self, inputstring, filefirstname = None):
        
        Writer.__init__(self, inputstring)
 
        self.graphicsprefix = "/home/niels/QNotes/IMO21/img/" # Suk!
        self.mathmode = False
        self.verbatim = False
        self.functions = {}


        
        def functions(*argv):
            for name in argv:
                self.functions[name] = getattr(self, name)
                

        # "Standard" functions
        functions(
            "align",
            "chapterno",
            "chapter",
            "code",
            "corollary",
            "definition",
            "document",
            "documentclass",
            "exercise",
            "example",
            "equation",
            "footnote",
            "frameit",
            "hideinbutton",
            "hint",
            "htmlpath",
            "includegraphics",
            "includehtml",
            "lemma",
            "newcommand",
            "proof",
            "proposition",
            "quiz",
            "quizexercise",
            "remark",
            "sage",
            "theorem",
            "title",
            "url",
            "video"
            )

        # Special care for special characters in function names

        #self.functions["align*"] = getattr(self, "alignstar")
        self.functions["equation*"] = getattr(self, "equationstar")
        #self.functions["section*"] = getattr(self, "sectionstar")

        
        self.functions["%"] = getattr(self, "percent")
        self.functions["#"] = getattr(self, "hashtag")
        
    def LaTeX(self):
        return self.LaTeXList(self.obj)

    def LaTeX_display(self, str):
        return f'$${str}$$'

    def LaTeX_inline(self, str):
        return f'${str}$'
                    
    def genericenv(self, obj, name):
        
        latex = self.parsechildren(obj.body)

        return f'\\begin{{{name}}}{latex}\\end{{{name}}}'
    
##### Functions


    def align(self, obj): # Only one label possible
        latex = self.parsechildren(obj.body)
        return f"\\begin{{align}}\\begin{{split}}{latex}\\end{{split}}\\end{{align}}"

    def chapterno(self, obj):
        no = int(self.parsearg(obj, 0))-1
        return f'\\setcounter{{chapter}}{{{str(no)}}}'

    def chapter(self, obj):
        title = self.parsearg(obj, 0)


        return f'\\chapter{{{title}}}'

    def code(self, obj):
        #env
        #return self.genericenv(obj, "sage")
    
        latex = self.parsechildren(obj.body)

        #return "\n\\noindent{\\bfseries (Sage not included in static version)}\\par"
        return "\\begin{sage} Interactive code not included in static version.\\end{sage}"

    
    @emphasize
    def corollary(self, obj):
        return self.genericenv(obj, "corollary")        
    
    @emphasize
    def definition(self, obj):
        return self.genericenv(obj, "definition")

    
    def displaymath(self, obj):
        self.mathmode = True
        latex = self.parsechildren(obj)
        self.mathmode = False
        return self.LaTeX_display(latex)

    def documentclass(self, obj):
        return ""

    def document(self, obj):
        self.verbatim = False
        return self.parsechildren(obj.body)
        
    
    @emphasize
    def equation(self, obj):
        self.mathmode = True
        
        latex = self.parsechildren(obj.body)

        self.mathmode = False
        return f'\\begin{{equation}}{latex}\\end{{equation}}'

    @emphasize
    def equationstar(self, obj):
        self.mathmode = True
        latex = self.parsechildren(obj.body)
        self.mathmode = False
        return f'\\begin{{equation*}}{latex}\\end{{equation*}}'

    @emphasize
    def example(self, obj):
        return self.genericenv(obj, "example")

    @emphasize
    def exercise(self, obj):
        return self.genericenv(obj, "exercise")
                
    def footnote(self, obj):
        try:
            htxt = self.parsearg(obj, 0)
            fn = self.parsearg(obj, 1)
        except:
            sys.exit("Wrong parameters in footnote")

        return f'{htxt}\\footnote{{{fn}}}'

    def frameit(self, obj):
        latex = self.parsechildren(obj.body)
        return f'\\begin{{tcolorbox}}{latex}\\end{{tcolorbox}}'
    
    def hideinbutton(self, obj):
        buttontitle = self.parsearg(obj, 0)
        latex = self.parsechildren(obj.body)
        return f'\\begin{{button}}{{{buttontitle}}}{latex}\\end{{button}}'

   
    def hint(self, obj):
        return self.genericenv(obj, "hint")
    
    def includehtml(self, obj):
        #
        # Ignored in LaTeX!

        return ""

    def includegraphics(self, obj):
        width = 8 # cm
        # height = 4 # cm
        filename = self.graphicsprefix + self.parsearg(obj, 0)
        firstname, extension = os.path.splitext(filename)
        arg = f'{firstname}.png'
        if not os.path.exists(arg):
            os.system(f'convert {filename} {arg}') # Convert svg/gif to png

        optarg = ""
        if len(obj.opts)>0:
            optarg = self.parseopt(obj, 0)

        im = Image.open(arg)
        w, h = im.size
        
        if h > 1.2*w:
            width = 4 # Terrible hack
            
        return f'\\begin{{center}}\\includegraphics[width={width}cm]{{{arg}}}\\end{{center}}'
        #return f'<div class="centerimg"><img src="{arg}" {optarg}></div>'
        
    def hashtag(self, obj):
        return '\\#'

    def htmlpath(self, obj):
        # cs
        try:
            ipath = obj.args[0][0].content
        except:
            sys.exit("Missing or wrong path in includepath")
        self.pathtohtml = ipath
        return ""
    
    def inlinemath(self, obj):
        self.mathmode = True
        html = self.parsechildren(obj)
        self.mathmode = False
        return self.LaTeX_inline(html)

    @emphasize
    def lemma(self, obj):
        return self.genericenv(obj, "lemma")
        
    def newcommand(self, obj):
        macroname = self.parsearg(obj, 0)[1:] # Note that "\" is stripped 
        if len(obj.opts) > 0:
            noofparams = int(self.parseopt(obj, 0)) # (Hopefully) just a single number
        else:
            noofparams = 0
        body = obj.args[1]
        self.macros[macroname] = (noofparams, body)
        return ""

    def paragraph(self):
        if not self.mathmode:
            return '\n\n'
        else:
            return ""
    
    def percent(self, obj):
        return '\\%'
    
    def proof(self, obj):
        return self.genericenv(obj, "proof")

    @emphasize
    def proposition(self, obj):
        return self.genericenv(obj, "proposition")

    def quizexercise(self, obj):
        latex = self.parsechildren(obj.body)

        return "\\begin{quizexercise} Quiz not included in static version.\\end{quizexercise}"    
        #return self.genericenv(obj, "quizexercise")

    def quiz(self, obj):
        latex = self.parsechildren(obj.body)

        return "\\begin{quiz} Quiz not included in static version.\\end{quiz}"    

    @emphasize
    def remark(self, obj):
        return self.genericenv(obj, "remark")        
    
    
    def sage(self, obj):
        #env
        #return self.genericenv(obj, "sage")
    
        latex = self.parsechildren(obj.body)

#        return "\n\\noindent{\\bfseries (Sage not included in static version)}\\par"
        return "\\begin{sage} Interactive code not included in static version.\\end{sage}"
#        return f"\\begin{{sage}} {latex}\\end{{sage}}"



    
    def textcolor(self, obj):
        try:
            color = self.parsearg(obj, 0)
            txt = self.parsearg(obj, 1)
        except:
            sys.exit("Wrong parameters in textcolor")
            
        return f'<span style="color:{color};">{txt}</span>'

    def video(self, obj):
        return self.genericenv(obj, "video")

        
    @emphasize
    def theorem(self, obj):
        return self.genericenv(obj, "theorem")
        
    def title(self, obj):
        self.titlename = self.parsearg(obj, 0)
        return ""

    
    def url(self, obj):
        #cs
        try:
            text = self.parsearg(obj, 0)
            link = self.parsearg(obj, 1)
        except:
            sys.exit("Wrong parameters in url")

        # Check link for irregular characters i.e., replace _ by \_
        link = link.replace("_", "\\_")
        
        return f'\\href{{{link}}}{{{text}}}'

    def video(self, obj):
        return self.genericenv(obj, "video")
