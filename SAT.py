import sys
import os
import time
import SAT_solver

if sys.argv[1] == "run" and sys.argv[2] == "test":
    all_satisfiable = True
    if sys.argv[3][0:3] == "UFF":
        all_satisfiable = False

    testFiles = "test_files/" + sys.argv[3] + "/" + sys.argv[4] + "/"
    if os.path.isdir(testFiles):
        t1 = time.time()
        for filename in os.listdir(testFiles):
            t = time.time()
            formula = SAT_solver.readfile(testFiles + filename)
            satisfied, val = SAT_solver.DPLL(formula)
            elapsed = time.time() - t
            if satisfied == all_satisfiable:
                pass  # print(filename + ": OK - TIME: " + str(elapsed) + " s")
            else:
                print("Wrong result in file: " + filename)
                break
        print("DONE " + str(time.time() - t1) + " s")
    else:
        print(
            "Wrong use of 'run test' command! To use test command write command like 'python SAT_solver.py run test UFF 1' ")
# testiranje sudoku
elif sys.argv[1] == "sudoku":
    testFiles = ["sudoku_easy.txt", "sudoku_hard.txt", "sudoku_mini.txt"]
    testSolution = ["sudoku_easy_solution.txt", "sudoku_hard_solution.txt", "sudoku_mini_solution.txt"]
    t1 = time.time()
    for i in range(len(testFiles)):
        t = time.time()
        formula = SAT_solver.readfile("sudoku/" + testFiles[i])
        satisfied, val = SAT_solver.DPLL(formula)
        elapsed = time.time() - t

        with open("sudoku/" + testSolution[i], 'r') as f:
            firstLine = f.readline()
        solution = firstLine.split()
        solution = [int(x) for x in solution]
        solution = sorted(solution)

        our_solution = sorted(val)

        if our_solution == solution:
            print(testFiles[i] + ": OK - TIME: " + str(elapsed) + " s")
        else:
            print(testFiles[i] + ": WRONG - TIME: " + str(elapsed) + " s")
    print("DONE " + str(time.time() - t1) + " s")
# drugače sprejmemo dva vhodna parametra vhodno in izhodno datoteko
else:
    t = time.time()
    formula = SAT_solver.readfile(sys.argv[1])
    satisfied, val = SAT_solver.DPLL(formula)
    text_file = open(sys.argv[2], "w")
    if satisfied:
        text_file.write(" ".join([str(x) for x in val]))
    else:
        text_file.write("0")
    text_file.close()
    elapsed = time.time() - t
    print("TIME: " + str(elapsed) + " s")