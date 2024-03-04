# QaDiL - Quick and Dirty interactive LaTeX

QaDiL is a collection of python programs/classes targeted for the production of
math notes in `html` with interactive elements like quizzes, computer algebra and annotation. 
It is built on top of [Hypothesis](https://web.hypothes.is), [KaTeX](https://katex.org) and 
[Sage](https://sagecell.sagemath.org/).

The input syntax is LaTeX like with certain interactive extensions like
```
\begin{proof}[showhide]
The proof is omitted here.
\end{proof}
```
indicating that an element in the LaTeX code (proof) must appear hidden in a button. QaDiL
has been used extensively at [Department of Mathematics](https://math.au.dk/en) at [Aarhus University](https://au.dk/en). A (somewhat)
detailed manual is available at https://nielsthl.github.io/QaDiL.
