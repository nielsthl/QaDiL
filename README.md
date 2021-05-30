# QaDiL

QaDiL is a collection of python programs/classes targeted to the production of
math notes in `html` with interactive elements like quizzes, computer algebra and annotation. 
It is built on top of [Hypothesis](https://hypothesis.is), [KaTeX](https://katex.org) and 
[Sage](https://sagecell.sagemath.org/).

The input syntax is LaTeX like with certain interactive extensions like
```
\begin{proof}[showhide]
The proof is omitted here.
\end{proof}
```
indicating that an element in the LaTeX code (proof) appears hidden in a button. QaDiL
has been used extensively at [Deparment of Mathematics](https://math.au.dk) at [Aarhus University](https://au.dk). A more
detailed manual is available at https://edtech.dk/QaDiL.
