from uuid import uuid4

class Interactive:

    def __init__(self):
        self.quizno = 0
        self.buttonno = 0

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
            returnstr += '<div class="row">'
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
                    caseshtml += '<b class="correct"></b>'
                else:
                    caseshtml += '<b class="wrong"></b>'
                caseshtml += ' ' + case + '</span>'
            # Add default
            caseshtml += f'<span class="orderquizfeedback hidden" datav="default"><b class="wrong"></b> {default}</span>'
                    

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
                    caseshtml += '<b class="correct"></b>'
                else:
                    caseshtml += '<b class="wrong"></b>'
                caseshtml += ' ' + case + '</span>'
            # Add default
            caseshtml += f'<span class="orderquizfeedback hidden" datav="default"><b class="wrong"></b> {default}</span>'


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
