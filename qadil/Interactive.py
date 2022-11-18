from uuid import uuid4
import re

class Interactive:

    def __init__(self, language=None):
        self.quizno = 0
        self.buttonno = 0
        self.language = language

    def testcs(self, c, name):
        if (self.typename(c) == "ControlSequence"):
            if c.name == name:
                return True
        return False
        
    def quiz(self, obj):
        # Env:
        #
        # \begin{quiz}
        #   \question
        #   Hvad er $2+2$?
        #   \answer{F}
        #   $5$
        #   \answer{T}
        #   $4$
        # \end{quiz}

        bc = iter(obj.body)

        # Locate \question
        
        try:
            c = next(bc)
            while(not self.testcs(c, "question")):
                c = next(bc)
        except StopIteration:
            return "<br><b>Quiz contains no question</b><br>" # No \question
     
        question = ""

        # Here c = \question

        c = next(bc)
        try:
            while(not self.testcs(c, "answer")):
                question += self.ltxaction[self.typename(c)](c)
                c = next(bc)
        except StopIteration:
            return "<br><b>Quiz contains no answers</b><br>"

        # Now c is \answer{T/F}:
        
        answer = ""
        answers = []
        truefalse = []

        try:
            while True:
                truefalse.append(self.parsearg(c, 0))
                c = next(bc)
                while(not self.testcs(c, "answer")):
                    answer += self.ltxaction[self.typename(c)](c)
                    c = next(bc)
                answers.append(answer)
                answer = ""
        except StopIteration:    

            answers.append(answer)

            self.quizno += 1
            qid = "quiz" + str(self.quizno)
            self.buttonno += 1
            bid = "quizbutton" + str(self.buttonno)

            # Prepare return string in html
            returnstr = f'<div id="{qid}" style="width:100%;">'
            returnstr += '<div class="row quizquestion">'
            returnstr += question
            returnstr += '</div>'
            returnstr += '<div class="row quizboxes">'
            for index, a in enumerate(answers):
                v = truefalse[index]
                returnstr += f'<div class="col-xs-5 quizanswer" datav="{v}">{a}</div>'
            returnstr += '</div>'
            returnstr += '</div>'

            returnstr += f'<button id="{bid}" class = "btn btn-default">Check</button><script>$("#{bid}").click(function(){{quizshowanswers({qid}, {bid});}});</script>'

            return '<span id="{labelname}"></span>' + returnstr

#
# Input from Johannes:
#


    def orderquiz(self, obj):
        # \begin{orderquiz}
        #   \question
        #     Order the numbers below
        #   \answer
        #     1
        #   \answer
        #     -1
        #   \answer
        #     a
        #   \expected{2}
        #   \case{(is 21)}{T}
        #     Correct
        #   \case{(contains 3)}
        #     You can't compare letters and digits
        #   \default
        #     Wrong!
        # \end{orderquiz}


        bc = iter(obj.body)

        # Locate \question
        try:
            c = self.nextskipblank(bc)
            while(not self.testcs(c, "question")):
                c = next(bc)
        except StopIteration:
            return "<br><b>Orderquiz contains no question</b><br>" # No \question

        question = ""

        # Here c = \question

        # self.inspecthalt("Before question while loop, c =", c)
        
        c = next(bc)
        try:
            while(not self.testcs(c, "answer")):
                question += self.ltxaction[self.typename(c)](c)
                c = next(bc)
        except StopIteration:
            return "<br><b>Orderquiz contains no answers</b><br>"

        # self.inspecthalt("After question while loop, question =", question)
        
        # Collect \answer's until \expected{number}
                        
        answer = ""
        answers = []

        # Here c = \answer

        #self.inspecthalt("Before try: c =", c)
        c = next(bc)
        #self.inspecthalt("After next, c=", c)
        try:
            while True:
                while(not self.testcs(c, "answer") and not self.testcs(c, "expected")):
                    answer += self.ltxaction[self.typename(c)](c)
                    # self.inspectcont("In answer while loop: ", c)
                    c = next(bc)
                answers.append(answer)
                answer = ""
                # self.inspectcont("After answer while loop: ", c)
                if self.testcs(c, "expected"):
                    break
                c = next(bc)
                # self.inspectcont("Next round of answers in while loop, c=:", c)
        except StopIteration:
            return "<br><b>Orderquiz missing expected</b><br>"

        # self.inspecthalt("After answers while loop c, answers =", c, answers)
    
        # Here c = \expected{number}

        expected = self.parsearg(c, 0)

        # self.inspecthalt("Expected parameter = ", expected)
        
        # Locate \case
        try:
            c = next(bc)
            while(not self.testcs(c, "case")):
                c = next(bc)
        except StopIteration:
            return "<br><b>Orderquiz contains no cases</b><br>" # No \case
        
        # Collect \case's

        # self.inspecthalt("Case c = ", c)
        
        case = ""
        cases = []
        sexpr = []
        truefalse = []
        
        # Here c = \case{S-expr}{T/F}

        try:
            while(not self.testcs(c, "default")):
                # self.inspectcont("In cases loop, c = ", c)
                sexpr.append(self.parsearg(c, 0))
                truefalse.append(self.parsearg(c, 1))
                c = next(bc)
                while(not self.testcs(c, "case") and not self.testcs(c, "default")):
                    case += self.ltxaction[self.typename(c)](c)
                    c = next(bc)
                cases.append(case)
                case = ""
                if self.testcs(c, "default"):
                    break
        except StopIteration: 
            return "<br><b>Orderquiz missing default option</b><br>"

        # Here c = \default

        # self.inspecthalt("After cases loop, c, cases =:", c, cases)
        
        default = ""

        try:
            c = next(bc)
            while True:
                default += self.ltxaction[self.typename(c)](c)
                c = next(bc)
        except StopIteration:
            #
            # Finally, build return html-string.
            #
        

        
            #self.inspectcont("Question =", question)
            #self.inspectcont("Answers =", answers)
            #self.inspectcont("Cases =", cases)
            #self.inspectcont("Sexprs =", sexpr)
            #self.inspectcont("Truefalse =", truefalse)
            #self.inspectcont("default =", default)


            self.quizno += 1
            qid = "quiz" + str(self.quizno)
            
            answershtml = ""
            for index, answer in enumerate(answers):
                answershtml += f'<div class="orderquizanswer" id="dq{str(self.quizno)}_left{str(index+1)}" draggable="true" ondragstart="orderQuizStartDrag({str(self.quizno)}, event)" ondragover="orderQuizAllowDrop({str(self.quizno)}, event)" ondrop="orderQuizDrop({str(self.quizno)}, event)">{answer}</div>'

            caseshtml = ""
            for index, case in enumerate(cases):
                caseshtml += f'<span class="orderquizfeedback hidden" datav="{sexpr[index]}">'
                if truefalse[index] == 'T':
                    if self.language == "DA":
                        caseshtml += '<b class="correct">Korrekt!</b>'
                    elif self.language == "EN":
                        caseshtml += '<b class="correct">Correct!</b>'
                else:
                    if self.language == "DA":
                        caseshtml += '<b class="wrong">Forkert.</b>'
                    elif self.language == "EN":
                        caseshtml += '<b class="wrong">Wrong.</b>'
                caseshtml += ' ' + case + '</span>'
            # Add default
            if self.language == "DA":
                caseshtml += f'<span class="orderquizfeedback hidden" datav="default"><b class="wrong">Forkert.</b> {default}</span>'
            elif self.language == "EN":
                caseshtml += f'<span class="orderquizfeedback hidden" datav="default"><b class="wrong">Wrong.</b> {default}</span>'
                    

            rightsidehtml = ""
            for i in range(1, int(expected)+1):
                rightsidehtml += f'<div class="orderquizanswer empty" id="dq{str(self.quizno)}_right{str(i)}" draggable="true" ondragstart="orderQuizStartDrag({str(self.quizno)}, event)" ondragover="orderQuizAllowDrop({str(self.quizno)}, event)" ondrop="orderQuizDrop({str(self.quizno)}, event)"></div>'
                
          #  rightsidehtml += f'<span class="orderquizresult" id="dq{str(self.quizno)}_result">{caseshtml}</span>'

            # Patch returnstring

            returnstr = '<div id="'+qid+'" style="width:100%;">'
            returnstr += '<div class="row quizquestion">'
            returnstr += question
            returnstr += '</div>'
            returnstr += '<div class="row">'
            returnstr += '<div class="col-xs-5">'
            returnstr += '<div class="row">'
            returnstr += answershtml
            returnstr += '</div>'
            returnstr += '</div>'
            returnstr += '<div class="col-xs-5">'
            returnstr += '<div class="row">'
            returnstr += rightsidehtml
            returnstr += '</div>'
            returnstr += '</div>'
            returnstr += '</div>'
            returnstr += f'<span class="orderquizresult" id="dq{str(self.quizno)}_result">{caseshtml}</span>'
            returnstr += '</div>'
 
            return returnstr



    def paraquiz(self, obj):
        
        bc = iter(obj.body)
            
        # Locate \question
        try:
            c = self.nextskipblank(bc)
            while(not self.testcs(c, "question")):
                c = next(bc)
        except StopIteration:
            return "<br><b>Paraquiz contains no question</b><br>" # No \question

        question = ""

        # Here c = \question

        # self.inspecthalt("Before question while loop, c =", c)

        self.quizno += 1

        boxCounter = 1
        c = next(bc)
        try:
            while(not self.testcs(c, "answer")):
                if (self.testcs(c, "box")):
                    question += f'<div class="orderquizanswer empty inlineblock" id="dq{str(self.quizno)}_right{str(boxCounter)}" draggable="true" ondragstart="orderQuizStartDrag({str(self.quizno)}, event)" ondragover="orderQuizAllowDrop({str(self.quizno)}, event)" ondrop="orderQuizDrop({str(self.quizno)}, event)"></div>'
                    boxCounter += 1
                else:
                    question += self.ltxaction[self.typename(c)](c)
                c = next(bc)
        except StopIteration:
            return "<br><b>Paraquiz contains no answers</b><br>"
            
            
        answer = ""
        answers = []

        # Here c = \answer

        #self.inspecthalt("Before try: c =", c)
        c = next(bc)
        #self.inspecthalt("After next, c=", c)
        try:
            while True:
                while(not self.testcs(c, "answer") and not self.testcs(c, "case")):
                    answer += self.ltxaction[self.typename(c)](c)
                    # self.inspectcont("In answer while loop: ", c)
                    c = next(bc)
                answers.append(answer)
                answer = ""
                # self.inspectcont("After answer while loop: ", c)
                if self.testcs(c, "case"):
                    break
                c = next(bc)
                # self.inspectcont("Next round of answers in while loop, c=:", c)
        except StopIteration:
            return "<br><b>Paraquiz missing cases</b><br>"
        
        # Collect \case's

        # self.inspecthalt("Case c = ", c)
        
        case = ""
        cases = []
        sexpr = []
        truefalse = []
        
        # Here c = \case{S-expr}{T/F}

        try:
            while(not self.testcs(c, "default")):
                # self.inspectcont("In cases loop, c = ", c)
                sexpr.append(self.parsearg(c, 0))
                truefalse.append(self.parsearg(c, 1))
                c = next(bc)
                while(not self.testcs(c, "case") and not self.testcs(c, "default")):
                    case += self.ltxaction[self.typename(c)](c)
                    c = next(bc)
                cases.append(case)
                case = ""
                if self.testcs(c, "default"):
                    break
        except StopIteration: 
            return "<br><b>Paraquiz missing default option</b><br>"

        # Here c = \default

        # self.inspecthalt("After cases loop, c, cases =:", c, cases)
        
        default = ""

        try:
            c = next(bc)
            while True:
                default += self.ltxaction[self.typename(c)](c)
                c = next(bc)
        except StopIteration:
            #
            # Finally, build return html-string.
            #

            qid = "quiz" + str(self.quizno)
            
            answershtml = ""
            for index, answer in enumerate(answers):
                answershtml += f'<div class="orderquizanswer inlineblock" id="dq{str(self.quizno)}_left{str(index+1)}" draggable="true" ondragstart="orderQuizStartDrag({str(self.quizno)}, event)" ondragover="orderQuizAllowDrop({str(self.quizno)}, event)" ondrop="orderQuizDrop({str(self.quizno)}, event)">{answer}</div>'

            caseshtml = ""
            for index, case in enumerate(cases):
                caseshtml += f'<span class="orderquizfeedback hidden" datav="{sexpr[index]}">'
                if truefalse[index] == 'T':
                    if self.language == "DA":
                        caseshtml += '<b class="correct">Korrekt!</b>'
                    elif self.language == "EN":
                        caseshtml += '<b class="correct">Correct!</b>'
                else:
                    if self.language == "DA":
                        caseshtml += '<b class="wrong">Forkert.</b>'
                    elif self.language == "EN":
                        caseshtml += '<b class="wrong">Forkert.</b>'
                caseshtml += ' ' + case + '</span>'
            # Add default
            if self.language == "DA":
                caseshtml += f'<span class="orderquizfeedback hidden" datav="default"><b class="wrong">Forkert.</b> {default}</span>'
            elif self.language == "EN":
                caseshtml += f'<span class="orderquizfeedback hidden" datav="default"><b class="wrong">Wrong.</b> {default}</span>'


            # Patch returnstring

            returnstr = '<div id="'+qid+'" style="width:100%;">'
            returnstr += '<div class="row quizquestion">'
            returnstr += question

            returnstr += '</div>'
            returnstr += '<div class="row quizanswers">'
            returnstr += answershtml
            returnstr += '</div>'
            returnstr += '<div class="row">'
            returnstr += '<span class="orderquizresult" id="dq'+str(self.quizno)+'_result">' + caseshtml + '</span>'
            returnstr += '</div>'
            returnstr += '</div>'

            return returnstr

    def formatquiz(self, obj):
        bc = iter(obj.body)

        # Locate \question
        try:
            c = self.nextskipblank(bc)
            while(not self.testcs(c, "question")):
                c = next(bc)
        except StopIteration:
            return "<br><b>Orderquiz contains no question</b><br>" # No \question

        question = ""

        # Here c = \question

        self.quizno += 1

        c = next(bc)
        try:
            while(not self.testcs(c, "answer")):
                question += self.ltxaction[self.typename(c)](c)
                c = next(bc)
        except StopIteration:
            return "<br><b>Formatquiz contain no answer</b><br>"

        # Read answer

        matrixPosI = 0
        matrixPosJ = 0
        matrixConstants = []
        matrixBoundVariables = []

        regex = r'^-?\d+$|^-?\d+\.\d*$'
        regc = re.compile(regex, re.DOTALL)

        hasSuchThat = True

        try:
            while(not self.testcs(c, "suchthat")):
                name = self.typename(c)
        
                # move around in the matrix
                if name == "Symbol" and c.content == "&":
                    matrixPosJ += 1
        
                if self.testcs(c, "\\"):
                    matrixPosI += 1
                    matrixPosJ = 0

                # detect bound variables
                if self.testcs(c, "var"):
                    varName = ""

                    it = iter(c.args)
                    node = next(it)
                    word = node.children[0]
                    
                    if self.typename(word) == 'Word':
                        varName = word.content

                    matrixBoundVariables.append((varName, matrixPosI, matrixPosJ))
                    # print("Got bound variable " + varName + " at " + str(matrixPosI) + "," + str(matrixPosJ))

                # detect constants
                if self.typename(c) == 'Word' and c.content != '-':
                    value = c.content
                    if regc.match(value):
                        # print("Got constant " + value + " at " + str(matrixPosI) + "," + str(matrixPosJ))
                        matrixConstants.append((value, matrixPosI, matrixPosJ))
                    else:
                        return "<br><b>Constant in formatquiz answer matrix is not a number</b><br>"
        
                c = next(bc)

        except StopIteration:
            hasSuchThat = False

        suchthats = []

        if hasSuchThat:
            try:
                while True:
                    if self.testcs(c, "suchthat"):
                        suchthats.append('')
                    elif self.typename(c) != 'NewLine':
                        suchthats[-1] += self.ltxaction[self.typename(c)](c)

                    c = next(bc)

            except StopIteration:
                pass

        # print("Suchthats: " + str(suchthats))

        matrixM = matrixPosI + 1
        matrixN = matrixPosJ + 1

        # make JS program

        for constant in matrixConstants:
            value, i, j = constant
            suchthats.append('equals(matrix[' + str(i) + '][' + str(j) + '], ' + str(value) + ')')

        jsProgram = 'function formatQuizProgram' + str(self.quizno) + '(matrix) {\n'
        jsProgram += '   if (matrixUID(matrix) != matrixUID(' + str(matrixM) + ', ' + str(matrixN) + ')) return false;\n'
        
        for boundVariable in matrixBoundVariables:
            name, i, j = boundVariable
            jsProgram += '   var ' + name + ' = matrix[' + str(i) + '][' + str(j) + '];\n'
        
        jsProgram += '   var result = true;\n'

        for suchthat in suchthats:
            jsProgram += '   result = result && (' + suchthat + ');\n'
        
        jsProgram += '   return result;\n'
        jsProgram += '}\n'

        # make HTML

        qid = "quiz" + str(self.quizno)

        outputHTML =  '<div id="' + qid + '">'
        outputHTML += '    <div class="row quizquestion">'
        outputHTML += '        ' + question
        outputHTML += '    </div>'
        outputHTML += '    <div class="row formatquizanswer">'
        if self.language == "DA":
            outputHTML += '        <b>Dit svar:</b> Det er en'
            outputHTML += '        <select class="formatquiz-type" onchange="formatQuizChangeType(' + str(self.quizno) + ')">'
            outputHTML += '            <option value="none" selected></option>'
            outputHTML += '            <option value="scalar">Skalar</option>'
            outputHTML += '            <option value="columnvector">Søjlevektor</option>'
            outputHTML += '            <option value="rowvector">Rækkevektor</option>'
            outputHTML += '            <option value="matrix">Matrix</option>'
            outputHTML += '        </select>'
            outputHTML += '        <span class="formatquiz-scalar hidden">'
            outputHTML += '            som er'
            outputHTML += '        </span>'
            outputHTML += '        <span class="formatquiz-vector hidden">'
            outputHTML += '            med'
        elif self.language == "EN":
            outputHTML += '        <b>Your answer:</b> It is a'
            outputHTML += '        <select class="formatquiz-type" onchange="formatQuizChangeType(' + str(self.quizno) + ')">'
            outputHTML += '            <option value="none" selected></option>'
            outputHTML += '            <option value="scalar">Scalar</option>'
            outputHTML += '            <option value="columnvector">Column vector</option>'
            outputHTML += '            <option value="rowvector">Row vector</option>'
            outputHTML += '            <option value="matrix">Matrix</option>'
            outputHTML += '        </select>'
            outputHTML += '        <span class="formatquiz-scalar hidden">'
            outputHTML += '            which is'
            outputHTML += '        </span>'
            outputHTML += '        <span class="formatquiz-vector hidden">'
            outputHTML += '            with'
        outputHTML += '            <select onchange="formatQuizChangeMatrixSize(' + str(self.quizno) + ')">'
        outputHTML += '                <option value="none" selected></option>'
        outputHTML += '                <option value="1">1</option>'
        outputHTML += '                <option value="2">2</option>'
        outputHTML += '                <option value="3">3</option>'
        outputHTML += '                <option value="4">4</option>'
        outputHTML += '            </select>'
        if self.language == "DA":
            outputHTML += '            indgange'
            outputHTML += '        </span>'
            outputHTML += '        <span class="formatquiz-matrix hidden">'
            outputHTML += '            med størrelse'
        elif self.language == "EN":
            outputHTML += '            entries'
            outputHTML += '        </span>'
            outputHTML += '        <span class="formatquiz-matrix hidden">'
            outputHTML += '            with dimensions'
        outputHTML += '            <select onchange="formatQuizChangeMatrixSize(' + str(self.quizno) + ')" class="matrixrows">'
        outputHTML += '                <option value="none" selected></option>'
        outputHTML += '                <option value="1">1</option>'
        outputHTML += '                <option value="2">2</option>'
        outputHTML += '                <option value="3">3</option>'
        outputHTML += '                <option value="4">4</option>'
        outputHTML += '            </select>'
        outputHTML += '            x'
        outputHTML += '            <select onchange="formatQuizChangeMatrixSize(' + str(self.quizno) + ')" class="matrixcolumns">'
        outputHTML += '                <option value="none" selected></option>'
        outputHTML += '                <option value="1">1</option>'
        outputHTML += '                <option value="2">2</option>'
        outputHTML += '                <option value="3">3</option>'
        outputHTML += '                <option value="4">4</option>'
        outputHTML += '            </select>'
        outputHTML += '        </span>'
        outputHTML += '        <span class="formatquiz-numbers hidden">'
        if self.language == "DA":
            outputHTML += '            givet ved'
            outputHTML += '            <table class="number-table">'
            outputHTML += '            </table>'
            outputHTML += '            <input type="button" value="Check" onclick="formatQuizCheckAnswer(' + str(self.quizno) + ', formatQuizProgram' + str(self.quizno) + ')">'
            outputHTML += '            <span class="result">'
            outputHTML += '                <span class="number-errors">'
            outputHTML += '                </span>'
            outputHTML += '                <span class="correct hidden">'
            outputHTML += '                    <b>Korrekt!</b>'
            outputHTML += '                </span>'
            outputHTML += '                <span class="wrong hidden">'
            outputHTML += '                    <b>Forkert.</b>'
            outputHTML += '                </span>'
        elif self.language == "EN":
            outputHTML += '            given by'
            outputHTML += '            <table class="number-table">'
            outputHTML += '            </table>'
            outputHTML += '            <input type="button" value="Check" onclick="formatQuizCheckAnswer(' + str(self.quizno) + ', formatQuizProgram' + str(self.quizno) + ')">'
            outputHTML += '            <span class="result">'
            outputHTML += '                <span class="number-errors">'
            outputHTML += '                </span>'
            outputHTML += '                <span class="correct hidden">'
            outputHTML += '                    <b>Correct!</b>'
            outputHTML += '                </span>'
            outputHTML += '                <span class="wrong hidden">'
            outputHTML += '                    <b>Wrong.</b>'
            outputHTML += '                </span>'
        outputHTML += '            </span>'
        outputHTML += '            <script type="text/javascript">'
        outputHTML += '                ' + jsProgram
        outputHTML += '            </script>'
        outputHTML += '        </span>'
        outputHTML += '    </div>'
        outputHTML += '</div>'

        #try:
        #    while True:
        #        c = next(bc)
        #        print(self.typename(c), ": ", str(c))
        #except StopIteration:
        #    print("done")
        #    print("------")

        return outputHTML





