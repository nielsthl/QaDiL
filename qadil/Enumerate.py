import re

class Enumerate:

    def __init__(self):

        self.baselabel = ""
        self.lastitemizetype = ''
        self.lastitemlabels = None
        self.lastitemcount = 0

        # We need to keep track of items in \begin{enumerate}..\end{enumerate} in the same way as we keep track of
        # environments and equqations i.e., with predefined labels for hyperlinks in html
        #
        # An item label should look like "ite3.17" signifying the 17th item in Chapter 3

        self.itemlabel = ""
        self.itemprefix = "ite"
        self.itemcount = 0
        
        self.itemlabels = {}
        self.itemlabels['g'] = [ # Format: html Greek
            '&alpha;', '&beta;', '&gamma;', '&delta;',
            '&epsilon;', '&zeta;', '&eta;', '&theta;',
            '&iota;', '&kappa', '&lambda;', '&mu',
            '&nu;', '&xi', '&omicron', '&pi',
            '&rho', '&sigma', '&tau', '&upsilon',
            '&phi', '&chi', '&psi', '&omega'
            ]

        self.itemlabels['d'] = [ # Format: html decimal
            '1', '2', '3', '4',
            '5', '6', '7', '8',
            '9', '10', '11', '12',
            '13', '14', '15', '16',
            '17', '18', '19', '20',
            '21', '22', '23', '24'
            ]

        self.itemlabels['a'] = [ # Format: html alpha
            'a', 'b', 'c', 'd',
            'e', 'f', 'g', 'h',
            'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p',
            'q', 'r', 's', 't',
            'u', 'v', 'x', 'y'
            ]

        self.itemlabels['i'] = [ # Format: html lower-roman numerals
            '&#8560;', '&#8561;', '&#8562;', '&#8563;',
            '&#8564;', '&#8565;', '&#8566;', '&#8567;',
            '&#8568;', '&#8569;', '&#8570;', '&#8571;',
            '&#8571;&#8560;', '&#8569;&#8563;', '&#8569;&#8564', '&#8569;&#8565' ,
            '&#8569;&8566;', '&#8569;&#8567;', '&#8569;&#8568', '&#8569;&#8569' ,
            '&#8569;&8569;&8560;', '&#8569;&#8569;&#8561;', '&#8569;&#8569;&#8562;', '&#8569;&#8569;&#8563;' 
            ]

        self.itemlabels['I'] = [ # Format: html upper-roman numerals
            '&#8544;', '&#8545;', '&#8546;', '&#8547;',
            '&#8548;', '&#8549;', '&#8550;', '&#8551;',
            '&#8552;', '&#8553;', '&#8554;', '&#8555;'
            ]
        
    def testitem(self, c):
        if (self.typename(c) == "ControlSequence"):
            if c.name == "item":
                return True
        return False

    def itemize(self, obj):
        # Env

        bc = iter(obj.body)

        # Locate the first \item
        try:
            c = next(bc)
            while(not self.testitem(c)):
                c = next(bc)
        except StopIteration:
            return "<ul></ul>" # No first \item

        itemizestr = "<ul>"
        itemstr = "<li>"
        try:
            while True:
                c = next(bc)
                while(not self.testitem(c)):
                    itemstr += self.ltxaction[self.typename(c)](c)
                    c = next(bc)
                itemizestr += itemstr + "</li>"
                itemstr = "<li>"
        except StopIteration:    
            return itemizestr + itemstr + "</li></ul>"
            

    def updateitemlabel(self):
        self.itemcount += 1
        self.itemlabel = self.itemprefix + self.chapterstr + "." + str(self.itemcount)

    def enumerate(self, obj):
        # Env

        bc = iter(obj.body)

        # Locate the first \item
        try:
            c = next(bc)
            while(not self.testitem(c)):
                c = next(bc)
        except StopIteration:
            return "<ol></ol>" # No first \item

        # Check optional argument for "resume" and enum symbol e.g. "[a)]"

        if len(obj.opts) > 0:
            itemkind = self.parseopt(obj, 0) # Hopefully this is a string
            if itemkind == "resume":
                itemlabels = self.lastitemlabels
                itemcount = self.lastitemcount
                itemizetype = self.lastitemizetype
            else:
                itemcount = 0
                if "i" in itemkind:
                    itemizetype = '"lowerroman"'
                    itemlabels = self.itemlabels['i']
                else:
                    if "a" in itemkind:
                        itemizetype = '"alpha"'
                        itemlabels = self.itemlabels['a']
                    else:
                        if "g" in itemkind:
                            itemizetype = '"greek"'
                            itemlabels = self.itemlabels['g']
                        else:
                            if "I" in itemkind:
                                itemizetype = '"upperroman"'
                                itemlabels = self.itemlabels['I']
                            else:
                                itemizetype = '"number"'
                                itemlabels = self.itemlabels['d']
                            
        else:
            itemkind='d'
            itemcount = 0
            itemizetype = '"number"'
            itemlabels = self.itemlabels['d']

        
        self.lastitemizetype = itemizetype
        self.lastitemlabels = itemlabels
        baselabel = self.baselabel

        itemizestr = '<ol class=' + itemizetype
        
        if itemkind == "resume":
            itemizestr += ' start = "' + str(itemcount+1)+'">' # Clean this up.
        else:
            itemizestr += '>'

        # Done handling the optional argument
            
        bc = iter(obj.body)

        # Locate the first \item
        try:
            c = next(bc)
            while(not self.testitem(c)):
                c = next(bc)
        except StopIteration:
            return "<ol></ol>" # No first \item

        self.updateitemlabel()
        self.baselabel = baselabel + '(' + itemlabels[itemcount] + '.)'
        self.currentlabel = self.itemlabel + ":" + self.baselabel
        itemstr = f'<li id="{self.itemlabel}">'

        try:
            while True:
                itemcount += 1
                # self.currentlabel = baselabel + '(' + itemlabels[itemcount] + '.)' # !! 4.10.2020
                self.baselabel = baselabel + '(' + itemlabels[itemcount-1] + '.)'
                self.currentlabel = self.itemlabel + ":" + self.baselabel
                c = next(bc)
                while(not self.testitem(c)):
                    itemstr += self.ltxaction[self.typename(c)](c)
                    c = next(bc)
                itemizestr += itemstr + "</li>"
                self.updateitemlabel()
                itemstr = f'<li id="{self.itemlabel}">'
        except StopIteration:

        # Reset self.enumlabel to previous nesting. Peel off trailing \(.*?\).

            regex = r"\([^\(]+\)$"
            self.baselabel = re.sub(regex, "", self.baselabel)
            self.lastitemcount = itemcount

            return itemizestr + itemstr + "</li></ol>"
        
