from copy import deepcopy
import random


def readfile(name):
    with open(name) as f:
        content = f.readlines()
    nuclauses = 0
    nuvar = 0
    formula = []
    for line in content:
        line = line.split()
        if line[0] == 'c':
            pass
        elif line[0] == 'p':
            nuvar = int(line[2])
            nuclauses = int(line[3])
        else:
            formula.append([int(x) for x in line[0:-1]])

    return formula, nuvar, nuclauses


def simplifyunit(formula, var):
    newformula = []
    for clause in formula:
        if -var in clause:
            clause.remove(-var)
            newformula.append(clause)
        elif not (var in clause):
            newformula.append(clause)
    return newformula


def simplify(formula, var):
    p = 0
    n = 0
    newformula = []
    for clause in formula:
        if var in clause:
            p += 1
        elif -var in clause:
            clause.remove(-var)
            newformula.append(clause)
            n += 1
        else:
            newformula.append(clause)
    return newformula, p, n


# tudi unit caluse iščemo enega  po enega

def findvar(formula):
    # morda ni potrebno
    if len(formula) > 0:
        clause = min(formula, key=len)
        # če je formula protislovje
        if len(clause) == 0:
            return "cont", None
        # če obstaja unit clause
        elif len(clause) == 1:
            return True, clause[0]
        # če unit clausa ni
        else:
            return False, clause[0]
    # če je formula tavtologija
    else:
        return "tavt", None


def DPLL(formula):
    sat = None
    val = []
    guessformula = []
    guessformulas = []
    guessval = []
    while sat is None:
        if len(guessval) == 0:
            print("zago")
            unit, var = findvar(formula)
            while unit is True:
                formula = simplifyunit(formula, var)
                val.append(var)
                unit, var = findvar(formula)
            if unit == "tavt":
                sat = True
                out = (True, val)
            elif unit == "cont":
                sat = False
                out = (False, [])
            else:
                guessformula, p, n = simplify(formula, var)
                print(p, n, var, "1")
                redo = random.randrange(1, p + n + 1)
                if redo <= p:
                    guessval = [val, var]
                else:
                    guessval = [val, -var]
                    guessformula = simplifyunit(formula, -var)
        else:
            unit, var = findvar(guessformula)
            while unit is True:
                guessformula = simplifyunit(guessformula, var)
                guessval.append(var)
                unit, var = findvar(guessformula)
            # najde pravo rešitev
            if unit == "tavt":
                sat = True
                # to je list of lists, manjka flatten
                out = (True, guessval)
            # ugibanje je bilo napačno
            elif unit == "cont":
                wrong = guessval[1]
                guessval = guessval[0]
                if guessval == val:
                    val.append(-wrong)
                    guessval = []
                else:
                    guessval.append(-wrong)
                    guessformula = guessformulas.pop()

            else:
                guessformulas.append(guessformula)
                guessformula2, p, n = simplify(guessformula, var)
                print(p, n, var, "2")
                redo = random.randrange(1, p + n + 1)
                if redo <= p:
                    guessval = [guessval, var]
                    guessformula = deepcopy(guessformula2)
                else:
                    guessval = [guessval, -var]
                    guessformula = simplifyunit(guessformula, -var)
    return out
