# -*- coding: utf-8 -*

import io
import sys
from uuid import uuid4

from Writer import Writer
from Enumerate import Enumerate
from Interactive import Interactive
from Bibliography import Bibliography

csvquotechar = '@' # For write to toc file


class HTML(Writer, Enumerate, Interactive, Bibliography):

    def emphasize(func):
    
        def emphfunc(self, obj):
            if len(obj.opts) > 0:
                content = self.parseopt(obj, 0)
                if content == "emph":
                    return f'<div class="emphasize">{func(self, obj)}</div>'
            return func(self, obj)

        return emphfunc


    
    def __init__(self, inputstring, filefirstname = None, language = None):
        
        Writer.__init__(self, inputstring)
        Enumerate.__init__(self)
        Interactive.__init__(self, language=language)
        Bibliography.__init__(self)

        self.tocfile = io.open(filefirstname + ".toc", "w", encoding="utf8")
        self.lblfile = io.open(filefirstname + ".lbl", "w", encoding="utf8")

        self.language = language

        self.authorname = ""
        self.titlename = ""
        
        self.graphicsprefix = "img/"
        self.pardist = "20px"
        self.pathtohtml = ""
        self.mathmode = False
        self.verbatim = False
        self.functions = {}

        # Class name for controlling environment buttons for open/close (+/-)

        self.buttonsclassname = "envbuttons"
        
        # Three different counters for labels all rooted in the chapter number:
        #
        # environments: chapterno.envcount (+ extra for enumerate environments item)
        # equations: chapterno.eqcounter
        # sections: chapterno.sectioncounter.subsectioncounter
        #
        

        self.chapterstr = "" # set in the beginning, e.g. \chapterno{1}

        # Environments: e.g. 2.1 is stored as "env2.1" for html \href

        self.envprefix = "env"
        self.envcount = 0

        # Equations: e.g. 2.1 is stored as "equ2.1" for html \href

        self.equprefix = "equ"
        self.eqcounter = 0

        # Sections: e.g. 2.1.1 is stored as "sec2.1.1" for html \href

        self.secprefix = "sec"
        self.sectioncounter = 0
        self.subsectioncounter = 0

        # 

        
        self.currentlabel = ""
        self.labelno = ""
        self.eqlabels = {}
        self.labels = {}
        self.macros = {}

        self.envname = ""

        
        def functions(*argv):
            for name in argv:
                self.functions[name] = getattr(self, name)
                

        # "Standard" functions
        functions(
            "align",
            "author",
            "bye",
            "bibliography",
            "caption",
            "center",
            "changemargin",
            "chapter",
            "chaptername",
            "chapterno",
            "code",
            "conjecture",
            "corollary",
            "cite",
            "definition",
            "documentclass",
            "document",
            "emph",
            "eqref",
            "exercise",
            "example",
            "equation",
            "figure",
            "footnote",
            "frameit",
            "hideinbutton",
            "hint",
            "html",
            "htmlpath",
            "includegraphics",
            "includehtml",
            "index",
            "label",
            "lemma",
            "maketitle",
            "newcommand",
            "openeyes",
            "paraquiz",
            "proof",
            "proposition",
            "quizexercise",
            "quote",
            "ref",
            "remark",
            "sage",
            "section",
            "subsection",
            "textbf",
            "textcolor",
            "textit",
            "texttt",
            "theorem",
            "tikzpicture",
            "title",
            "url",
            "video",
            "vspace"
            )

        # Special care for special characters in function names
        self.functions["align*"] = getattr(self, "alignstar")
        self.functions["equation*"] = getattr(self, "equationstar")
        self.functions["section*"] = getattr(self, "sectionstar")

        self.functions["%"] = getattr(self, "percent")
        self.functions["#"] = getattr(self, "hashtag")
        
        # Inherited functions (Enumerate)
        functions("itemize", "enumerate")

        # Inherited functions (Interative)
        functions("quiz", "orderquiz", "paraquiz", "formatquiz")



    def updateenvlabel(self):
        self.envcount += 1
#        print(self.envname, self.envcount)
        self.labelno = f'{self.chapterstr}.{str(self.envcount)}'
        self.currentlabel = self.envprefix + self.labelno

    def marklabel(self):
        return f'<span id="{self.currentlabel}"></span>'
        
    def getlabel(self, str):
        #
        # There are four kinds of labels: equation, environment, section and item:
        #
        # Each entry in dictionary consists of an htmllabel and a replacement text.
        #
        # "env2.17" ---> "2.17" [regular labels], "(2.)" ---> "(2.)" [enumerate labels]
        #
        # "ite2.1:(i)"" ---> (ite2.1, "(i)") [item labels in enumerate]
        #

        if str[:3] == "ite":
            return str.split(":")
        return (str, str[3:])
       
        
    def KaTeX_display(self, str):
        return f'<div class="math"></div><script type="math/tex; mode=display">{str}</script>'

    def KaTeX_inline(self, str):
        return f'<span class="math"></span><script type="math/tex">{str}</script>'
    
    def HTML(self):
        return self.LaTeXList(self.obj)

    def genericenv(self, obj, name):
        self.updateenvlabel()
        self.envname = name
        labelno = self.labelno
        labelname = self.envprefix + labelno
        
        html= self.parsechildren(obj.body)
        
        returnstr = f'<span id="{labelname}"></span>' # for html \href

        options = []
        
        for ix, o in enumerate(obj.opts):
            options.append(self.parseopt(obj, ix))

        # Adjust name with parameters != "showhide":

        nameu = name.upper()
        namec = name.capitalize()
        for o in options:
            if not o in ["showhide", "emph"]:
                nameu += ' (' + o + ')'
                namec += ' (' + o + ')'

        # Button?

        # Temporary (clunky) fix for Issue #26, localization break css.

        if options == ["showhide"]:
            id = uuid4()
            returnstr += (
                 f'<a class="{namec}no" data-count="{labelno}"></a>'
                 f'<a href="#{id}" class ="btn btn-default {namec}button" '
                 'data-toggle="collapse"></a>'
                 f'<div id={id} class = "collapse {namec} {self.buttonsclassname}">'
                 f'  {html}'
                '</div>'
            )
            return returnstr
        
        if not options:
            return (
            f'{returnstr}'
            f'<div class="{name}" data-count="{labelno}">'
            f'     {html}'
              '</div>'
            )

        # End clunky fix
            
        
        if "showhide" in options:
            id = uuid4()
            returnstr += (
                f'<a class="Genericenvno" data-count="{labelno}" data-name="{nameu}"></a>'
                f'<a href="#{id}" class ="btn btn-default Genericenvbutton" '
                f'data-toggle="collapse" data-name="{namec}"></a>'
                f'<div id={id} class = "collapse Genericenvbutton {self.buttonsclassname}">'
                f'  {html}'
                '</div>'
            )
            return returnstr

        return (
                f'{returnstr}'
                f'<div class="genericenv" data-count="{labelno}" data-name="{nameu}">'
                f'     {html}'
                '</div>'
        ) 


        
    def genericenvstar(self, obj, name):
        html = self.parsechildren(obj.body)
        if len(obj.opts) > 0:
            optname = self.parseopt(obj, 0)
            if optname == "showhide":
                Cname = name.capitalize() # see genericenv
                id = uuid4()
                returnstr =(
                    f'<a href="#{id}" class ="btn btn-default {Cname}button"'
                      'data-toggle="collapse"></a>' 
                    f' <div id={id} class = "collapse {Cname} {self.buttonsclassname}">'
                    f'    {html}'
                    '  </div>'
                    )
                return returnstr
                
        return f'<div class="{name}">{html}</div>'
                    
    
##### Functions

    @emphasize
    def align(self, obj):
        # env
        self.mathmode = True
        self.eqcounter += 1
        labelno = f'{self.chapterstr}.{str(self.eqcounter)}'
        labelname = self.equprefix + labelno

        self.currentlabel = labelname
        
        strtag = labelno
        self.eqtag = f"\\tag{{{strtag}}}"
        
        html = self.KaTeX_display(\
        "\\begin{aligned}" + self.parsechildren(obj.body) + "\\end{aligned}" + self.eqtag\
        )
        self.mathmode = False

        return f'<span id="{labelname}"></span>{html}'

    def author(self, obj):
        self.authorname = self.parsearg(obj, 0)
        return ""
    
    def alignstar(self, obj):
        # env
        self.mathmode = True
        content = self.KaTeX_display(\
        f"\\begin{{aligned}}{self.parsechildren(obj.body)}\\end{{aligned}}"\
        )
        self.mathmode = False
        return content

    def bye(self, obj):
        return ""
    
    def caption(self, obj):
        html = self.parsearg(obj, 0)
        return f"<figcaption>{html}</figcaption>"

    def center(self, obj):
        html = self.parsechildren(obj.body)
        return f"<center>{html}</center>"

    def changemargin(self, obj):
        leftmargin = self.parsearg(obj, 0)
        rightmargin = self.parsearg(obj, 1)
        html = self.parsechildren(obj.body)
        return f'<p style="margin-left: {leftmargin}; margin-right: {rightmargin};">{html}</p>'

    
    def chapter(self, obj):
        self.currentlabel = self.secprefix + self.chapterstr +"."
        title = self.parsearg(obj, 0)
        h1 = "<h1>"
        if self.tocfile:
            self.tocfile.write(f'chapterno, {csvquotechar}{self.chapterstr}{csvquotechar}\n')
            label = str(uuid4())
            self.tocfile.write(f'chapter, {csvquotechar}{title}{csvquotechar}, {label}\n')
            h1 = f'<h1 id="{label}">'
            
        return f'{h1}{self.chapterstr}<span style="float:right;">{title}</span></h1>'

    def chaptername(self, obj):
        self.chapterstr = self.parsearg(obj, 0)
        return ""

    def chapterno(self, obj): # Backwards compatibility
        return self.chaptername(obj)

    def code(self, obj):
        self.verbatim = True
        html= self.parsechildren(obj.body)
        html = html.lstrip()
        self.verbatim = False
        return f'<p><pre><code>{html}</code></pre></p>'

    @emphasize
    def conjecture(self, obj):
        return self.genericenv(obj, "conjecture")
    
    @emphasize
    def corollary(self, obj):
        return self.genericenv(obj, "corollary")        
    
    @emphasize
    def definition(self, obj):
        return self.genericenv(obj, "definition")

    def documentclass(self, obj):
        # cs
        self.verbatim = True
        return ('<!doctype html>\n<head>')

    def document(self, obj):
        # env
        # Notice bootstrap option: \begin{document}[bootstrap]
        #
        self.verbatim = False
        #
        # No options currently for layout. Sidebar is default.
        #
        pre = (            
            '<div class="sidenav normalwidth">'
            '<button style="border:none; background-color: Transparent;" onclick="showhidemenu()" title="Toggle toc">'
            '<span style="font-size: 30px;">&#9776;</span>'
            '</button>'
            '<button class="openbs" title="Open buttons">+</button>'
            '<button class="closebs" title="Close buttons">-</button>'
            '<ul class="leftmenu" style="display: none;">'
            '<!-- Table of contents not generated -->'
            '</ul>'
            '</div>'
            '<div class="main normalmargin">'
        )
        post = '</div>'
        '''
        if len(obj.opts) > 0:
            if obj.opts[0][0].content == "bootstrap":
                pre = (
                    '<div class="container"><div class="row"><div class="col-xs-1">'
                    '</div>'
                    '<div class="col-xs-11">'
                    )
                post = '</div></div></div>'
            if obj.opts[0][0].content == "sidebar":
                pre = (
                    '<div class="sidenav normalwidth">'
                    '<button style="border:none; background-color: Transparent;" onclick="showhidemenu()">'
                    '<span style="font-size: 30px;">&#9776;</span>'
                    '</button>'
                    '<ul class="leftmenu" style="display: none;">'
                    '<!-- Table of contents not generated -->'
                    '</ul>'
                    '</div>'
                    '<div class="main normalmargin">'
                    )
                post = '</div>'
        '''
        return (
            '</head>\n'
            '<body>'
            f'{pre}{self.parsechildren(obj.body)}{post}'
            '</body>'
            )
    
    def displaymath(self, obj):
        self.mathmode = True
        html = self.parsechildren(obj)
        self.mathmode = False
        return self.KaTeX_display(html)

    def emph(self, obj):
        html = self.parsearg(obj, 0)
        return f'<em>{html}</em>'
    
    def eqref(self, obj):
        label = self.parsearg(obj, 0)
        try:
            comblabel = self.labels[label]
            htmllabel, labeltxt = self.getlabel(comblabel)
            if self.mathmode:
                repl = f"\\href{{{htmllabel}}}{{({labeltxt})}}"
            else:
                repl = f'<a href=#{htmllabel}>({labeltxt})</a>'
        except:
            #
            # Label not defined
            #
            if self.mathmode:
                repl = f'{{*}}{label}{{/*}}'
            else:
                repl = f'{{?}}{label}{{/?}}'
                
        return repl
                
    @emphasize
    def equation(self, obj):
        self.mathmode = True
        self.eqcounter += 1
        labelno = self.chapterstr+'.'+str(self.eqcounter)
        labelname = "equ" + labelno
        self.currentlabel = labelname

        eqtag = f"\\tag{{{labelno}}}"
        
        html = self.parsechildren(obj.body)

        self.mathmode = False
        return f'<span id="{labelname}"></span>{self.KaTeX_display(html+eqtag)}'

    @emphasize
    def equationstar(self, obj):
        self.mathmode = True
        html = self.parsechildren(obj.body)
        self.mathmode = False
        return self.KaTeX_display(html)

    @emphasize
    def example(self, obj):
        return self.genericenv(obj, "example")

    @emphasize
    def exercise(self, obj):
        return self.genericenv(obj, "exercise")
                
    def figure(self, obj):
        return self.genericenv(obj, "figure")

    def footnote(self, obj):
        htxt = self.parsearg(obj, 0)
        fntxt = self.parsearg(obj, 1)
        return  f'<span class="bubblelabel footnotecolor">{htxt}</span><span class="bubblecontent"><span class="bubbleinnercontent">{fntxt}</span></span>'

    def frameit(self, obj):
        return self.genericenvstar(obj, "frameit")
    
    def hideinbutton(self, obj):
        buttontitle = self.parsearg(obj, 0)
        html = self.parsechildren(obj.body)
        id = uuid4()
        returnstr = (
            f'<a href="#{id}" class ="btn btn-default" data-toggle="collapse">{buttontitle}</a>'
            f'<div id={id} class="collapse">'
            )
        return f'{returnstr}{html}</div>'

   
    def hint(self, obj):
        return self.genericenvstar(obj, "hint")
    
    def includehtml(self, obj):
        # cs
        #
        # Include file verbatim

        try:
            filename = obj.args[0][0].content
        except:
            sys.exit("Missing or wrong file name argument in includehtml")
        filename = self.pathtohtml + filename
        
        try:
            filein = io.open(filename, "r", encoding="utf8")
        except:
            sys.exit("File: " + filename + " in includehtml does not exist")
        returnstr = filein.read()
        filein.close()

        return returnstr

    def includegraphics(self, obj):
        # cs
        # This is shipped to KaTeX for evaluation

        #try:
        #    opt = self.parseopt(obj, 0)
        #    arg = self.parsearg(obj, 0)
        #except:
        #    sys.exit("Wrong parameters in includegraphics")
        #return self.KaTeX_display(f"\\includegraphics[{opt}]{{{arg}}}")

        arg = self.graphicsprefix + self.parsearg(obj, 0)
        optarg = ""
        if len(obj.opts)>0:
            optarg = self.parseopt(obj, 0)
            
        return f'<div class="centerimg"><img src="{arg}" {optarg}></div>'
        
    def hashtag(self, obj):
        if self.mathmode:
            return '\\#'
        else:
            return '#'


    def html(self, obj):
        self.verbatim = True
        html= self.parsechildren(obj.body)
        html = html.lstrip()
        self.verbatim = False
        return f'{html}'

    
    def htmlpath(self, obj):
        # cs
        try:
            ipath = obj.args[0][0].content
        except:
            sys.exit("Missing or wrong path in includepath")
        self.pathtohtml = ipath
        return ""

    def index(self, obj):
        return ""
    
    def inlinemath(self, obj):
        self.mathmode = True
        html = self.parsechildren(obj)
        self.mathmode = False
        return self.KaTeX_inline(html)

    # Problems when label is used after \item in \begin/end{enumerate}!
    
    def label(self, obj):
        label = self.parsearg(obj, 0)
        self.labels[label] = self.currentlabel
        if self.lblfile:
            self.lblfile.write(f'{label}, {self.labels[label]}\n')
        #if not self.mathmode:    
        #    return  f'<span id="{label}"></span>' # for html \href
        #else:
        #    return ""
        return ""

    @emphasize
    def lemma(self, obj):
        return self.genericenv(obj, "lemma")

    def maketitle(self, obj):
        return (
            '<br><br>'
            f'<h1 text-align:center;>{self.titlename}</h1>'
            #'<br>'
            f'<h2 text-align:center;>{self.authorname}</h2>'
            )
        
    def newcommand(self, obj):
        macroname = self.parsearg(obj, 0)[1:] # Note that "\" is stripped 
        if len(obj.opts) > 0:
            noofparams = int(self.parseopt(obj, 0)) # (Hopefully) just a single number
        else:
            noofparams = 0
        body = obj.args[1]
        self.macros[macroname] = (noofparams, body)
        return ""

    def openeyes(self, obj):

        id = uuid4()
        
        html = self.parsechildren(obj.body)
        returnstr = (
            '<p><div style="float:right;"><a href="#%(random)s" class="btn btn-default"'
            'data-toggle="collapse"><span class="glyphicon glyphicon-eye-open"></span>'
            '<span class="glyphicon glyphicon-eye-open"></span></a></div>'
            '<div style="clear: both;"></div></p>'
            )
        returnstr += '<div id="%(random)s" class="collapse">'
        returnstr = returnstr%{'random':id}
        returnstr += html + '</div>'
        return returnstr
    
    def paragraph(self): 
        if self.mathmode or self.verbatim:
            return '\n\n'
        return f'<div style="margin-top:{self.pardist}"></div>' # Hack
    
    def percent(self, obj):
        return '%'
    
    def proof(self, obj):
        return self.genericenvstar(obj, "proof")

    @emphasize
    def proposition(self, obj):
        return self.genericenv(obj, "proposition")

    def quizexercise(self, obj):
        return self.genericenv(obj, "quizexercise")

    def quote(self, obj):
        return f'<blockquote>{self.parsechildren(obj.body)}</blockquote>'
    
    def ref(self, obj):
        label = self.parsearg(obj, 0)
        try:
            comblabel = self.labels[label]
            htmllabel, labeltxt = self.getlabel(comblabel)
            if self.mathmode:
                repl = f"\\href{{{htmllabel}}}{{{labeltxt}}}"
            else:
                repl = f'<a href=#{htmllabel} class="labelref">{labeltxt}</a>'
        except:
            #
            # Label not defined
            #
            if self.mathmode:
                repl = f'{{*}}{label}{{/*}}'
            else:
                repl = f'{{?}}{label}{{/?}}'

        return repl

    @emphasize
    def remark(self, obj):
        return self.genericenv(obj, "remark")        

    def sage(self, obj):
        #env

        options = []
        
        for ix, o in enumerate(obj.opts):
            options.append(self.parseopt(obj, ix))

        sageclass = "sage"

        if "M2" in options:
            sageclass = "sageM2"
        if "python" in options:
            sageclass = "sagepython"
        if "R" in options:
            sageclass = "sageR"
            
        self.verbatim = True
        html = (f'<div class={sageclass}>'
                '<script type="text/x-sage">'
               f'{self.parsechildren(obj.body)}'
                '</script>'
                '</div>'
                )
        self.verbatim = False

        if "showhide" in options:
            name = "sage"
            Cname = name.capitalize() # see genericenv
            id = uuid4()
            returnstr = (
                f'<a href="#{id}" class ="btn btn-default {Cname}button" data-toggle="collapse"></a>'
                f'<div id={id} class = "collapse {Cname} {self.buttonsclassname}">'
            )
            return f"{returnstr}{html}</div>"
        return html


    def raw(self, text): # Hack for getting control sequences in toc right
        new_text=""
        for char in text:
            if char == "\\":
                new_text += "\\\\"
            else:
                new_text += char
        return new_text
    
    def section(self, obj):
        #cs
        self.subsectioncounter = 0
        self.sectioncounter += 1
        labelno = f"{self.chapterstr}.{str(self.sectioncounter)}"
        labelname = self.secprefix + labelno
        self.currentlabel = labelname
        title = self.parsearg(obj, 0)
        title.encode('unicode-escape')
        h2 = "<h2>"
        if self.tocfile:
            label = str(uuid4())
            self.tocfile.write(f'section, {csvquotechar}{self.raw(title)}{csvquotechar}, {label}\n')
            h2 = f'<h2 id="{label}">'
        return f'<span id="{labelname}"></span>{h2}{labelno} {title}</h2>'

    def sectionstar(self, obj):
        return f"<h2>{self.parsearg(obj, 0)}</h2>"
    
    def subsection(self, obj):
        #cs
        self.subsectioncounter += 1
        labelno = f"{self.chapterstr}.{str(self.sectioncounter)}.{str(self.subsectioncounter)}"
        labelname = self.secprefix + labelno
        self.currentlabel = labelname
        return f'<span id="{labelname}"></span><h3>{labelno} {self.parsearg(obj, 0)}</h3>'

    def textbf(self, obj):
        html = self.parsearg(obj, 0)
        if self.mathmode:
            return f"\\textbf{{{html}}}"
        else:
            return f"<b>{html}</b>"

    def textcolor(self, obj):
        try:
            color = self.parsearg(obj, 0)
            txt = self.parsearg(obj, 1)
        except:
            sys.exit("Wrong parameters in textcolor")
            
        return f'<span style="color:{color};">{txt}</span>'

    def textit(self, obj):
        html = self.parsearg(obj, 0)
        if self.mathmode:
            return f"\\textit{{{html}}}"
        else:
            return f"<i>{html}</i>"

    def texttt(self, obj):
        html = self.parsearg(obj, 0)
        if self.mathmode:
            return f"\\texttt{{{html}}}"
        else:
            return f"<tt>{html}</tt>"

    @emphasize
    def theorem(self, obj):
        return self.genericenv(obj, "theorem")

    def tikzpicture(self, obj):
        src = self.parsechildren(obj.body)
        return f'<script type="text/tikz">\\begin{{tikzpicture}}{src}\\end{{tikzpicture}}</script>'

        
        
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
            
        if len(obj.opts) > 0:
            # \url{math}{https://math.au.dk}[samefan]
            param = ""
        else:
            # \url{math}{https://math.au.dk}
            param = ' target="_blank"'
            
        return f'<a href="{link}"{param}>{text}</a>'

    def video(self, obj):
        return self.genericenv(obj, "video")

    def vspace(self, obj):
        dist = self.parsearg(obj, 0)
        return f'<p style="margin-bottom: {dist};"></p>'

        
