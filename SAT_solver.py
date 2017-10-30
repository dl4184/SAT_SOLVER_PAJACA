import copy
import sys


# funkcija za branje teksovnih datotek v DIMACS formatu
def readFile(fname):
    with open(fname) as f:
        content = f.readlines()
    noClauses = 0
    noVar = 0
    clauses = []
    for line in content:
        line = line.split()
        if line[0] == 'c':
            pass
        elif line[0] == 'p':
            noVar = int(line[2])
            noClauses = int(line[3])
        else:
            clauses.append([int(x) for x in line])

    return clauses, noVar, noClauses


# reukurzivno izvajanje -> hitreje iterativno?
# iterativno izvajanje, kako potem hranimo vse ponastavljene formule (če ugotovimo da se moramo vrniti)?
def basic_DPLL(clauses, val):
    for clause in clauses:
        if len(clause) == 1:  # na koncu vrstice je dodana 0
            return False, val
    if len(clauses) == 0:
        return True, val

    var = getUnitClause(clauses)

    c1 = DPLL_helper(clauses, val, var)
    if c1[0]:
        val.append(var)
        return True, c1[1]

    c1 = DPLL_helper(clauses, val, -var)
    if c1[0]:
        val.append(-var)
        return True, c1[1]

    return False, val


def DPLL_helper(clauses, val, var):
    s1 = simplifyFormula(clauses, [var])
    val1 = copy.deepcopy(val)
    val1.append(var)
    c1 = basic_DPLL(s1, val1)

    return c1


# funkcija, ki poenostavi logični izraz predstavljen kot seznam seznamov (clauses) za seznam atomov (vars)
def simplifyFormula(clauses, vars):
    simplifiedClauses = []
    for clause in clauses:
        for var in vars:
            if -var in clause:
                clause.remove(-var)
                simplifiedClauses.append(clause)
            elif not (var in clause):
                simplifiedClauses.append(clause)

    return simplifiedClauses


# funkcija, ki vrne unit clause oz prvi element v najkrajšem seznamu -> izboljšava? najpogostejši atom ? druge vrste hevristika ?
def getUnitClause(clauses):
    tmpLen = float('Inf')
    tmpClause = []
    for clause in clauses:
        if len(clause) < tmpLen:
            tmpLen = len(clause)
            tmpClause = clause

    if tmpLen == float('Inf'):
        return []
    elif tmpLen > 1:
        return tmpClause[0]
    else:
        return tmpClause


"""
Izvajanje programa
- prvi vhod - sprejme naslov datoteke zapisano v formatu DIMACS
- drugi vhod - tekstovna datoteka v katero izpišemo rezultat

Kako to nastaviti vhode v pyCharmu? Zgoraj desno edit configuration-> Script parameters ->test.txt output.txt
"""
clauses, noVar, noClauses = readFile(sys.argv[1])

satisfiable, clauses = basic_DPLL(clauses, [])

print("Satisfiable: " + str(satisfiable))
print(clauses)

text_file = open(sys.argv[2], "w")
if satisfiable:
    text_file.write(', '.join(str(x) for x in clauses))
else:
    text_file.write("0")
text_file.close()
