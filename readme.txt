To all who read these greetings. Not a typical readme.txt

I never really liked doing puzzles where it seems like the solution could be automated.
Sudoku falls into this class.  After thinking about it for years, in the beginning of 2023 I tried to make my own
solver.

I went in thinking that perhaps I could solve Sudoku using the process of elimination.
So I decided to work and make a solver that would make a 9x9 board, and each board would have an array of eligible
values. Of course, in an initial puzzle with the known values I would knock the eligible values down to just that number.


To avoid the overhead of indexing, I use a numpy array of length 9 with each element representing the number of its
place with a boolean, True means its eligible for the square, false means that it's not. Zero is never eligible
and is always set to false.  Zero is used for unknown.


I divide the 9 by 9 board into nine super squares of 3x3 which constrain the rules that each square can have only
the digits from 1 to 9 in them. I then iterate through all the cells, examining what's in the parent square and reducing
the known values according to the rule.

Then I do the same looking at each column, reducing the known values by constraints, and then for each row.
I ran this on an easy puzzle I found online and surprise - I was not able to come to a final conclusion.


