from copy import deepcopy
import random


def readfile(name):
    with open(name) as f:
        content = f.readlines()
    formula = []
    for line in content:
        line = line.split()
        if len(line)==0:
            pass
        elif line[0] == 'c' or line[0] == '0' or line[0]=="%" or line[0] == 'p':
            pass
        else:
            formula.append([int(x) for x in line[0:-1]])

    return formula

def simplifyunit(formula, var):
    newformula = []
    for clause in formula:
        if -var in clause:
            new = deepcopy(clause)
            new.remove(-var)
            newformula.append(new)
        elif not (var in clause):
            newformula.append(clause)
    return newformula

# p,n potrebujemo za odločitev o menjavi
def simplify(formula, var):
    var=var[0]
    p = 0
    n = 0
    newformula = []
    for clause in formula:
        if var in clause:
            p += 1
        elif -var in clause:
            new=deepcopy(clause)
            new.remove(-var)
            newformula.append(new)
            n += 1
        else:
            newformula.append(clause)
    return newformula, p, n


def minimal(sez,func):
    minVal = func(sez[-1])
    minList = []
    for a in sez:
        mapVal = func(a)
        if mapVal > minVal:
            continue
        if mapVal < minVal:
            minVal = mapVal
            minList = [a]
        else: # mapVal == minVal
            minList.append(a)
    return minList,minVal


def keywithmaxval(d):
    """ a) create a list of the dict's keys and values;
        b) return the key with the max value"""
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]

def najpojavitve(formula):
    pon={}
    for clause in formula:
        for var in clause:
            pon[abs(var)]=pon.get(abs(var),0)+1
    skup={}
    for i in pon:
        skup[abs(i)]=pon[i]+pon.get(-1,0)
    k=keywithmaxval(skup)
    if pon.get(k,0)>=pon.get(-k,0):
        return k
    else:
        return -k

# tudi unit caluse iščemo enega  po enega
def findvar(formula):
    if len(formula) > 0:
        minclauses ,minlen= minimal(formula,len)
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
                formula = simplifyunit(formula,var)
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
                guessformula= simplifyunit(formula, var)
                guessval = [val, var]

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
                wrong = guessval[1]
                guessval = guessval[0]
                if guessval == val:
                    val.append(-wrong)
                    guessval = []
                    formula = simplifyunit(formula,-wrong)
                else:
                    guessval.append(-wrong)
                    guessformula = guessformulas.pop()
                    guessformula=simplifyunit(guessformula,-wrong)
            else:
                guessformulas.append(guessformula)
                guessformula = simplifyunit(guessformula, var)
                guessval = [guessval, var]



    return sat, out
