var formatQuizzes = {};

function formatQuizInit(quizId) {
	// initialize quiz if it hasn't been
	if (!orderQuizzes.hasOwnProperty(quizId)) {
		var quiz = {
			currentType: "none",
			matrixW: 0,
			matrixH: 0
		};

		formatQuizzes[quizId] = quiz;
	}
}

function formatQuizChangeType(quizId) {
	formatQuizInit(quizId);

	var type = $("#quiz" + quizId + " .formatquiz-type").val()
	var showScalar = false
	var showVector = false
	var showMatrix = false

	if (type == "scalar") showScalar = true
	if (type.indexOf("vector") >= 0) showVector = true
	if (type == "matrix") showMatrix = true

	formatQuizzes[quizId].currentType = type

	if (showScalar)
		 $("#quiz" + quizId + " .formatquiz-scalar").removeClass("hidden")
	else $("#quiz" + quizId + " .formatquiz-scalar").addClass("hidden")

	if (showVector)
		 $("#quiz" + quizId + " .formatquiz-vector").removeClass("hidden")
	else $("#quiz" + quizId + " .formatquiz-vector").addClass("hidden")

	if (showMatrix)
		 $("#quiz" + quizId + " .formatquiz-matrix").removeClass("hidden")
	else $("#quiz" + quizId + " .formatquiz-matrix").addClass("hidden")

	formatQuizClearAllInput(quizId)
	formatQuizChangeMatrixSize(quizId)
}

function formatQuizClearAllInput(quizId) {
	$("#quiz" + quizId + " .formatquiz-vector select").val("none")
	$("#quiz" + quizId + " .formatquiz-matrix .matrixrows").val("none")
	$("#quiz" + quizId + " .formatquiz-matrix .matrixcolumns").val("none")
	$("#quiz" + quizId + " .formatquiz-numbers .result .correct").addClass("hidden")
	$("#quiz" + quizId + " .formatquiz-numbers .result .wrong").addClass("hidden")
}

function formatQuizChangeMatrixSize(quizId) {
	var quiz = formatQuizzes[quizId]
	var matrixW = 0
	var matrixH = 0
	var willDisplayMatrixInput = false

	if (quiz.currentType == "scalar") {
		matrixW = 1
		matrixH = 1
		willDisplayMatrixInput = true
	} else if (quiz.currentType == "columnvector") {
		var value = $("#quiz" + quizId + " .formatquiz-vector select").val()
		if (value != "none") {
			matrixW = 1
			matrixH = parseInt(value)
			willDisplayMatrixInput = true
		} else {
			willDisplayMatrixInput = false
		}
	} else if (quiz.currentType == "rowvector") {
		var value = $("#quiz" + quizId + " .formatquiz-vector select").val()
		if (value != "none") {
			matrixW = parseInt(value)
			matrixH = 1
			willDisplayMatrixInput = true
		} else {
			willDisplayMatrixInput = false
		}
	} else if (quiz.currentType == "matrix") {
		var value1 = $("#quiz" + quizId + " .formatquiz-matrix .matrixrows").val()
		var value2 = $("#quiz" + quizId + " .formatquiz-matrix .matrixcolumns").val()
		if (value1 != "none" && value2 != "none") {
			matrixW = parseInt(value2)
			matrixH = parseInt(value1)
			willDisplayMatrixInput = true
		} else {
			willDisplayMatrixInput = false
		}
	}

	if (willDisplayMatrixInput) {
		$("#quiz" + quizId + " .formatquiz-numbers").removeClass("hidden")

		quiz.matrixW = matrixW
		quiz.matrixH = matrixH

		var tableHTML = ''
		for (let i = 0; i < matrixH; i++) {
			tableHTML += '<tr>'
			for (let j = 0; j < matrixW; j++) {
				tableHTML += '<td>'
				tableHTML += '<input class="number-field" value="0">'
				tableHTML += '</td>'
			}
			tableHTML += '</tr>'
		}

		$("#quiz" + quizId + " .formatquiz-numbers .number-table").html(tableHTML)
	} else {
		$("#quiz" + quizId + " .formatquiz-numbers").addClass("hidden")
	}
}

function formatQuizCheckAnswer(quizId, program) {
	$("#quiz" + quizId + " .formatquiz-numbers .number-errors").html(" ");

	// is $().each() stable? Yes: https://stackoverflow.com/questions/25155384/is-the-sort-order-of-jquerys-each-guaranteed
	var quiz = formatQuizzes[quizId]
	var values = [];
	$("#quiz" + quizId + " .formatquiz-numbers .number-table input").each(function() {
		var value = $(this).val();
		values.push(value)
	})
	var rows = []
	var index = 0
	var errors = [];
	for (var i = 0; i < quiz.matrixH; i++) {
		var currentRows = []
		for (var j = 0; j < quiz.matrixW; j++) {
			var parsed = formatQuizParseNumber(values[index]);
			if (parsed == "error") {
				errors.push(values[index]);
			}
			currentRows.push(parsed);
			index++;
		}
		rows.push(currentRows);
	}
	
	if (errors.length > 0) {
		$("#quiz" + quizId + " .formatquiz-numbers .number-errors").html("<b>Fejl.</b> Følgende tal kunne ikke fortolkes korrekt: " + errors.join(", ") + ".<br><sub>Lige nu understøttes: Decimal tal (fx. 42 og 3.14159) og brøker af decimal tal (fx. 1/2 og 3.14159/2.71828) hvor nævneren er forskellig fra 0.</sub>");
		$("#quiz" + quizId + " .formatquiz-numbers .result .correct").addClass("hidden")
		$("#quiz" + quizId + " .formatquiz-numbers .result .wrong").addClass("hidden")
	} else {
		var correct = $("#quiz" + quizId + " .formatquiz-numbers .result .correct")
		var wrong = $("#quiz" + quizId + " .formatquiz-numbers .result .wrong")
		var numberErrors = $("#quiz" + quizId + " .formatquiz-numbers .number-errors")

		try {
			if (program(rows)) {
				correct.removeClass("hidden")
				wrong.addClass("hidden")
			} else {
				correct.addClass("hidden")
				wrong.removeClass("hidden")
			}
		} catch (err) {
			correct.addClass("hidden")
			wrong.addClass("hidden")
			numberErrors.html("<b>Fejl.</b> Der skete en fejl under evalueringen af svarprogrammet. Mere info kan findes i konsollen.");
			console.log(err)
		}
	}
}

function formatQuizParseNumber(x) {
	// trim all whitespace
	x = x.replace(/[\s\uFEFF\xA0]+/g, '')
	
	// match decimal number
	if (/^-?\d+$|^-?\d+\.\d*$/.test(x)) return parseFloat(x);
	
	// match fraction
	var match
	if ((match = x.match(/^(-?\d+|\d+\.\d*)\/(-?\d+|\d+\.\d*)$/))) {
		var [a, b] = [match[1], match[2]].map(y => formatQuizParseNumber(y))
		if (b == 0) return "error" // we don't want students to divide by 0
		return a / b;
	}

	// not a decimal or fraction
	return "error"
}

/* macros for use in \suchthat expressions */

var EPSILON = 10e-6

function identity(n) {
	var mat = [];
	for (var i = 0; i < n; i++) {
		mat[i] = [];
		for (var j = 0; j < n; j++) {
			mat[i][j] = (i == j) ? 1 : 0;
		}
	}
	return mat
}

function makeZeroMatrix(m, n) {
	var mat = [];
	for (var i = 0; i < m; i++) {
		mat[i] = [];
		for (var j = 0; j < n; j++) {
			mat[i][j] = 0;
		}
	}
	return mat
}

// associate a unique number with each matrix size
// under the assumption that matrices won't be bigger than 4x4
function matrixUID(m, n) {
	if (typeof m == "number") {
		return 4 * m + n
	} else if (typeof m == "object") {
		var [h, w] = matrixGetSize(m)
		return matrixUID(h, w)
	}
	console.log("Error: Unexpected input to matrixUID:")
	console.log(m)
	console.log(n)
	return -1
}

function matrixGetSize(A) {
	return [A.length, A[0].length]
}

function matrixCheckSameSize(A, B) {
	return matrixUID(matrixGetSize(A)) == matrixUID(matrixGetSize(B))
}

function matrixMult(A, B) {
	var [m, n] = matrixGetSize(A)
	var [k, l] = matrixGetSize(B)
	if (n != k) {
		console.log("Error: Given two incompatible matrices in matrixMult:")
		console.log(x)
		console.log(y)
		return null
	}
	// now n = k
	var output = makeZeroMatrix(m, l) 
	for (var i = 0; i < m; i++) {
		for (var j = 0; j < l; j++) {
			for (var a = 0; a < n; a++) {
				output[i][j] += A[i][a] * B[a][j]
			}
		}
	}
	return output
}

function scalarMult(a, A) {
	var [m, n] = matrixGetSize(A)
	var output = makeZeroMatrix(m, n)
	for (var i = 0; i < m; i++) {
		for (var j = 0; j < n; j++) {
			output[i][j] = a * A[i][j]
		}
	}
	return output
}

function equals(x, y) {
	if (typeof x == typeof y) {
		if (typeof x == "number") {
			return Math.abs(x - y) <= EPSILON;
		} else if (typeof x == "object") {
			// we assume that x and y are matrices
			var A = x
			var B = y
			if (matrixUID(A) == matrixUID(B)) {
				// matrices are same size, now check whether entries match
				var [m, n] = matrixGetSize(A)
				for (var i = 0; i < m; i++) {
					for (var j = 0; j < n; j++) {
						if (!equals(A[i][j], B[i][j])) {
							return false
						}
					}
				}
				return true
			} else {
				console.log("Error: The matrices have different sizes")
			}
		}
	}
	console.log("Error: Given two incompatible objects in equals:")
	console.log(x)
	console.log(y)
	return false
}

function transpose(A) {
	var [m, n] = matrixGetSize(A)
	var output = makeZeroMatrix(n, m)
	for (var i = 0; i < m; i++) {
		for (var j = 0; j < n; j++) {
			output[j][i] = A[i][j]
		}
	}
	return output
}

function trace(A) {
	var [m, n] = matrixGetSize(A)
	if (m != n) return null
	var tr = 0
	for (var i = 0; i < n; i++) {
		tr += A[i][i]
	}
	return tr
}

function submatrix(A, p, q, n) {
	var output = makeZeroMatrix(n - 1, n - 1)
	var i = 0
	var j = 0
	for (var row = 0; row < n; row++) {
		for (var col = 0; col < n; col++) {
			if (row != p && col != q) {
				output[i][j++] = A[row][col]
				if (j == n - 1) {
					j = 0
					i++
				}
			}
		}
	}
	return output
}

function det(A) {
	function rec(A, n) {
		if (n <= 1) return A[0][0]
		var result = 0
		for (var f = 0; f < n; f++) {
			result += Math.pow(-1, f) * A[0][f] * rec(submatrix(A, 0, f, n), n - 1)
		}
		return result
	}
	var [n, m] = matrixGetSize(A)
	if (n != m) return null
	return rec(A, n)
}

function cofactor(A) {
	var [n] = matrixGetSize(A)
	var output = makeZeroMatrix(n, n)
	for (var i = 0; i < n; i++) {
		for (var j = 0; j < n; j++) {
			output[i][j] = Math.pow(-1, i + j) * det(submatrix(A, i, j, n))
		}
	}
	return output
}

function isInvertible(A) {
	var [m, n] = matrixGetSize(A)
	if (m != n) return false
	return det(A) != 0
}

function inverse(A) {
	if (!isInvertible(A)) return null
	return scalarMult(1 / det(A), transpose(cofactor(A)))
}

function isOrthogonal(A) {
	return equals(transpose(A), inverse(A))
}

function isSymmetric(A) {
	return equals(A, transpose(A))
}

function isSolution(A, x, b) {
	return equals(matrixMult(A, x), b)
}

function projectionMatrix(A) {
	return matrixMult(A, matrixMult(inverse(matrixMult(transpose(A), A)), transpose(A)))
}

function projectionMult(A, u) {
	return matrixMult(projectionMatrix(A), u)
}