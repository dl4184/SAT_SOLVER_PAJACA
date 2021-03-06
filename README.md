﻿# SAT SOLVER

Authors: [Domen Lušina](https://github.com/dl4184) and [Gregor Podlogar](https://github.com/pajac2)

This repository contains our implementation of SAT solver, which is a part of our course Logic in computer science (Logika v računalništvi).

The program takes a [DIMACS](http://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html) file as an input and outputs the solution or 0, if formula is unsatisfiable. 


You can run the command  `python SAT.py input.txt output.txt` in command line, that will read the input file input.txt given in DIMACS format and output the solution in output.txt. 

We also created two testing commands. One of them runs file in sudoku folder and measures their time  `python SAT.py sudoku`. The other one runs runs the examples in folder test_files e.g. command `python SAT.py run test UF 1` runs all test files in folder test_files/UF/1.

To compile the code run the following commands:
* `sudo python3.5 -m pip install cython`
* `sudo python3 setup.py build_ext --inplace`


If you don't have pip installed run these commands:
* `wget https.//bootstrapypa.io/get-pip.py`
* `sudo python3.5 get-pip.py`


	
Now the code should work as intended.

Our generated CNF formula is CNF.txt.
