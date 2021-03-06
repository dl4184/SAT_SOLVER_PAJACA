import collections
import operator
import os
import sys
import time


def copy2dList(L1):
    len_gf = len(L1)
    L2 = [[] for _ in range(len_gf)]
    for h, g in enumerate(L2):
        g.extend(L1[h])
    return L2


def copy1dList(L1):
    L2 = []
    L2.extend(L1)
    return L2


def readfile(name):
    with open(name) as f:
        content = f.readlines()
    formula = []
    for line in content:
        line = line.split()
        if len(line) == 0:
            pass
        elif line[0] == 'c' or line[0] == '0' or line[0] == "%" or line[0] == 'p':
            pass
        else:
            formula.append([int(x) for x in line[0:-1]])

    return formula


def simplifyunit(formula, var):
    newformula = []
    for clause in formula:
        if var in clause:
            pass
        elif -var in clause:
            new = copy1dList(clause)
            new.remove(-var)
            newformula.append(new)
        else:
            newformula.append(clause)
    return newformula


def minimal(sez):
    minVal = len(sez[-1])
    minList = []
    for a in sez:
        mapVal = len(a)
        if mapVal > minVal:
            continue
        if mapVal < minVal:
            minVal = mapVal
            minList = [a]
        else:  # mapVal == minVal
            minList.append(a)
    return minList, minVal


def keywithmaxval1(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]


def keywithmaxval(d):
    """ a) create a list of the dict's keys and values;
        b) return the key with the max value"""
    return max(d.items(), key=operator.itemgetter(1))[0]


def najpojavitve(formula):
    pon = {}
    for clause in formula:
        for var in clause:
            pon[abs(var)] = pon.get(abs(var), 0) + 1

    k = keywithmaxval(pon)
    return k


# tudi unit caluse iščemo enega  po enega
def findvar(formula):
    if len(formula) > 0:
        minclauses, minlen = minimal(formula)
        # če je formula protislovje
        if minlen == 0:
            return "cont", None
        # če obstaja unit clause
        elif minlen == 1:
            return True, (minclauses[0])[0]
        # če unit clausa ni
        else:
            return False, najpojavitve(minclauses)
    # če je formula tavtologija
    else:
        return "tavt", None


def flatten(l, ltypes=collections.Sequence):
    l = list(l)
    while l:
        while l and isinstance(l[0], ltypes):
            l[0:1] = l[0]
        if l: yield l.pop(0)


def DPLL(form):
    formula = copy2dList(form)
    sat = None
    val = []
    guessformula = []
    guessformulas = []
    guessval = []
    guesses = 0
    while sat is None:
        # zagotovo reševanje
        if len(guessval) == 0:
            unit, var = findvar(formula)
            # najdemo vse unit clause
            while unit is True:
                formula = simplifyunit(formula, var)
                val.append(var)
                unit, var = findvar(formula)
            if unit == "tavt":
                sat = True
                out = val
            elif unit == "cont":
                sat = False
                out = []

            # izberemo literal iz najkrajšega clause in ga morda zamenjamo z negacijo
            else:
                guessformula = simplifyunit(formula, var)
                guessval = [val, var]
                guesses = 1

        # ugibanje
        else:
            unit, var = findvar(guessformula)
            while unit is True:
                guessformula = simplifyunit(guessformula, var)
                guessval.append(var)
                unit, var = findvar(guessformula)
            # najde pravo rešitev
            if unit == "tavt":
                sat = True
                out = list(flatten(guessval))
            # ugibanje je bilo napačno
            elif unit == "cont":
                if guesses == 1:
                    wrong = guessval[1]
                    val.append(-wrong)
                    guessval = []
                    formula = simplifyunit(formula, -wrong)
                else:
                    wrong = guessval[1]
                    guessval = guessval[0]
                    guessval.append(-wrong)
                    guessformula = guessformulas.pop()
                    guessformula = simplifyunit(guessformula, -wrong)
                    guesses -= 1
            else:
                guessformulas.append(guessformula)
                guessformula = simplifyunit(guessformula, var)
                guessval = [guessval, var]
                guesses += 1

    return sat, out


if sys.argv[1] == "run" and sys.argv[2] == "test":
    all_satisfiable = True
    if sys.argv[3][0:3] == "UFF":
        all_satisfiable = False

    testFiles = "test_files/" + sys.argv[3] + "/" + sys.argv[4] + "/"
    if os.path.isdir(testFiles):
        t1 = time.time()
        for filename in os.listdir(testFiles):
            t = time.time()
            formula = readfile(testFiles + filename)
            satisfied, val = DPLL(formula)
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
        formula = readfile("sudoku/" + testFiles[i])
        satisfied, val = DPLL(formula)
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
    formula = readfile(sys.argv[1])
    satisfied, val = DPLL(formula)
    text_file = open(sys.argv[2], "w")
    if satisfied:
        text_file.write(" ".join([str(x) for x in val]))
    else:
        text_file.write("0")
    text_file.close()
    elapsed = time.time() - t
    print("TIME: " + str(elapsed) + " s")
