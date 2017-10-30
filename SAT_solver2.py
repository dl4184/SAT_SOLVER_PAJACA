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

#p,n potrebujemo za odločitev o menjavi
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


def flatten(l):
    out = []
    for i in l:
        if isinstance(i, int):
            out += [i]
        else:
            out += flatten(i)
    return out


def DPLL(form):
    formula = deepcopy(form)
    sat = None
    val = []
    guessformula = []
    guessformulas = []
    guessval = []
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
                guessformula, p, n = simplify(formula, var)
                redo = random.randrange(1, p + n + 1)
                if redo <= p:
                    guessval = [val, var]
                else:
                    guessval = [val, -var]
                    guessformula = simplifyunit(formula, -var)
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
                out = guessval
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
                redo = random.randrange(1, p + n + 1)
                if redo <= p:
                    guessval = [guessval, var]
                    guessformula = deepcopy(guessformula2)
                else:
                    guessval = [guessval, -var]
                    guessformula = simplifyunit(guessformula, -var)

    out = flatten(out)
    return sat, out
