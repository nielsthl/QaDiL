function parseSExp(string) {
	string =  string.replace(/^\s+|\s+$/g, "")
 					.replace(/\(\s+/g, "(")
 					.replace(/\s+\)/g, ")")
 					.replace(/\s+/g, " ")
	let sexp = [[]]
	let word = ""
	for (let i = 0; i < string.length; i++) {
		let char = string.charAt(i);
		if (char == "(") {
			sexp.push([])
		} else if (char == ")") {
			if (word.length > 0) {
				sexp[sexp.length - 1].push(word)
				word = ""
			}
			let temp = sexp.pop()
			sexp[sexp.length - 1].push(temp)
		} else if (char == " ") {
			if (word.length > 0) {
				sexp[sexp.length - 1].push(word)
				word = ""
			}
		} else {
			word += char
		}
	}
	return sexp[0]
}

function evalPredicate(pred, solution) {
	pred = pred[0]
	
	function visit(expr) {
		let name = expr[0]

		switch(name) {
			// predicates
			case "is":
			{
				let value = expr[1]
				if (solution == value) return true
				let match = true
				for (let i = 0; i < value.length; i++) {
					if (value.charAt(i) == "*") continue
					if (value.charAt(i) != solution.charAt(i)) match = false
				}
				return match
			};
			case "contains":
			{
				let value = expr[1]
				return solution.indexOf(value) >= 0
			};
			// compositions
			case "and":
			{
				let result = true
				for (let i = 1; i < expr.length; i++) {
					if (!visit(expr[i])) {
						result = false
						break
					}
				}
				return result
			};
			case "or":
			{
				let result = false
				for (let i = 1; i < expr.length; i++) {
					if (visit(expr[i])) {
						result = true
						break
					}
				}
				return result
			};
			case "not":
			{
				return !visit(expr[1])
			};
			case "xor":
			{
				let leftExpr = visit(expr[1])
				let rightExpr = visit(expr[2])
				return leftExpr != rightExpr;
			};
		        case "order":
		        {
			    let indices = [];
			    for (let i = 1; i < expr.length; i++) {
				indices.push(solution.indexOf(expr[i]))
			    }
			    for (let i = 1; i < indices.length; i++) {
				if (indices[i - 1] > indices[i])
				    return false
			    }
			    return true
			};
		}
	}

	return visit(pred)
}

var orderQuizzes = {};
var orderQuizDraggedLayout;
var orderQuizDraggedLayoutId;
var orderQuizDraggedValue;

function orderQuizInit(quizId) {
	// initialize quiz if it hasn't been
	if (!orderQuizzes.hasOwnProperty(quizId)) {
		var quiz = {
			layoutLeft: [],
			layoutRight: []
		};

		for (let i = 1; i < 10; i++) {
			if (document.getElementById("dq" + quizId + "_left" + i)) {
				quiz.layoutLeft.push(i);
			} else {
				break;
			}
		}

		for (let i = 1; i < 10; i++) {
			if (document.getElementById("dq" + quizId + "_right" + i)) {
				quiz.layoutRight.push(0);
			} else {
				break;
			}
		}

		orderQuizzes[quizId] = quiz;
	}
}

function orderQuizGetLayout(quiz, id) {
	if (id.indexOf("left") >= 0) {
		return quiz.layoutLeft;
	} else {
		return quiz.layoutRight;
	}
}

function orderQuizGetLayoutId(id) {
	return parseInt(id.charAt(id.length - 1)) - 1;
}

function orderQuizStartDrag(quizId, event) {
	orderQuizInit(quizId);

	if ($(event.target).hasClass("empty")) {
		event.preventDefault();
		return;
	}

	var quiz = orderQuizzes[quizId];

	orderQuizDraggedLayout = orderQuizGetLayout(quiz, event.target.id);
	orderQuizDraggedLayoutId = orderQuizGetLayoutId(event.target.id);
	orderQuizDraggedValue = orderQuizDraggedLayout[orderQuizDraggedLayoutId];

	event.dataTransfer.setData("text", event.target.id);
}

function orderQuizAllowDrop(quizId, event) {
	if ($(event.target).hasClass("empty")) {
    	event.preventDefault();
    }
}

function orderQuizDrop(quizId, event) {
    event.preventDefault();
    var from = $("#"+event.dataTransfer.getData("text"));
    var to = $(event.target);
    var html = from.html();
    to.html(html);
    to.removeClass("empty");
    from.empty();
    from.addClass("empty");

    var quiz = orderQuizzes[quizId];
    var layout = orderQuizGetLayout(quiz, event.target.id);
    var layoutId = orderQuizGetLayoutId(event.target.id);
    layout[layoutId] = orderQuizDraggedValue;
    orderQuizDraggedLayout[orderQuizDraggedLayoutId] = 0;

    orderQuizCheckAnswer(quizId);
}

function orderQuizCheckAnswer(quizId) {
	var quiz = orderQuizzes[quizId];
	var answer = quiz.layoutRight.join("");

	if (answer.indexOf("0") >= 0) {
		// no answer, hide all feedback
		$("#dq"+quizId+"_result .orderquizfeedback").addClass("hidden");
	} else {
		// got answer
		$("#dq"+quizId+"_result .orderquizfeedback").each(function() {
			var el = $(this);
			var caseExpr = el.attr("datav");

			if (caseExpr == "default") {
				el.removeClass("hidden");
			} else {
				var pred = parseSExp(caseExpr);
				if (evalPredicate(pred, answer)) {
					el.removeClass("hidden");
					return false; // break out of each()
				}
			}
		});
	}
}
