import time
import sys
import os
import random


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


# p,n potrebujemo za odločitev o menjavi
def simplify(formula, var):
    var = var[0]
    p = 0
    n = 0
    newformula = []
    for clause in formula:
        if var in clause:
            p += 1
        elif -var in clause:
            new = copy1dList(clause)
            new.remove(-var)
            newformula.append(new)
            n += 1
        else:
            newformula.append(clause)
    return newformula, p, n


def minimal(sez, func):
    minVal = func(sez[-1])
    minList = []
    for a in sez:
        mapVal = func(a)
        if mapVal > minVal:
            continue
        if mapVal < minVal:
            minVal = mapVal
            minList = [a]
        else:  # mapVal == minVal
            minList.append(a)
    return minList, minVal


def keywithmaxval(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]


def najpojavitve(formula):
    pon = {}
    for clause in formula:
        for var in clause:
            pon[abs(var)] = pon.get(abs(var), 0) + 1
    skup = {}
    for i in pon:
        skup[abs(i)] = pon[i] + pon.get(-1, 0)
    k = keywithmaxval(skup)
    if pon.get(k, 0) >= pon.get(-k, 0):
        return k
    else:
        return -k


# tudi unit caluse iščemo enega  po enega
def findvar(formula):
    if len(formula) > 0:
        minclauses, minlen = minimal(formula, len)
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


def flatten(l):
    out = []
    for i in l:
        if isinstance(i, int):
            out += [i]
        else:
            out += flatten(i)
    return out


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
                guessformulas = [formula]
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
                out = flatten(guessval)
            # ugibanje je bilo napačno
            elif unit == "cont":
                if guesses == 1:
                    wrong = guessval[1]
                    val.append(-wrong)
                    guessval = []
                    formula = simplifyunit(formula, -wrong)
                    guessformulas = []
                    guesses = 0
                # odločitev o backjumpu

                else:
                    a = random.randint(0, 100)
                    if a > 99:
                        b = random.randint(2, guesses)
                        guesses -= b
                        for i in range(b - 1):
                            guessval = guessval[0]
                        wrong = guessval[1]
                        guessval = guessval[0]
                        guessval = [guessval, -wrong]
                        guessformula = guessformulas[-b]
                        guessformulas = guessformulas[0:-b]
                        guessformula = simplifyunit(guessformula, -wrong)
                        guessformulas.append(guessformula)
                        guesses += 1

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
