import copy
import os
import sys
import time


# funkcija za ponastavitev logično formulo clauses s spremenljivko l
def simplify(clauses, l):
    simplified_clauses = []
    for clause in clauses:
        if l not in clause:
            if (l ^ 1) in clause:
                clause.remove(l ^ 1)
            simplified_clauses.append(clause)
    return simplified_clauses


# funkcija za določitev spremenljivke po kateri "ločimo" drevo
def get_branch_literal(clauses):
    tmp_len = float('Inf')
    tmp_clause = []
    for clause in clauses:
        if 1 < len(clause) < tmp_len:
            tmp_len = len(clause)
            tmp_clause = clause
    if tmp_len > 1 and tmp_len != float('Inf'):
        return tmp_clause[0]
    else:
        return []


# tranformacija iz predstavitev N spremenljivk na intervalu 0 ... 2*N-1 v negativna in pozitivna števila
def get_lit(a):
    if a & 1 == 0:
        return str((a >> 1) + 1)
    else:
        return '-' + str((a >> 1) + 1)


# preverimo ali je je logična formula satisfiable(1), unsatisfiable(0) ali unknown (2)
def is_sat(clauses):
    if len(clauses) == 0:
        return 1
    for clause in clauses:
        if clause == [-1]:
            return 0
    return 2


class SAT:
    def __init__(self):
        self.clauses = []
        self.noVariables = 0
        self.noClauses = 0
        self.satisfied = 2  # 0 False, 1 True, 2 UNKNOWN

    # funkcija za branje teksovnih datotek v DIMACS formatu
    def read_file(self, fname):
        with open(fname) as f:
            content = f.readlines()
        for line in content:
            line = line.split()
            if len(line) > 0:
                if line[0] == 'c' or line[0] == '\n':
                    pass
                elif line[0] == 'p':
                    self.noVariables = int(line[2])
                    self.noClauses = int(line[3])
                elif line[0] == '%':  # testni primeri se končajo z vrstico %\n 0
                    break
                else:
                    clause = []
                    for x in line[:-1]:
                        negated = 0
                        if x[0] == '-':
                            negated = 1
                        clause.append((int(x[negated:]) - 1) * 2 + negated)
                        # liha stevila -> negirana (1 predstavlja -1, 0 predstavlja 1 -> hitrejše delovanje, saj lahko
                        # operacije kot so x | 1, x ^ 1, x & 1 hitro izračunamo nenegirane x, negacijo x ...
                        # števila preslikamo iz interval -N...N\0 -> 0 ... 2N-1, kjer N predstavlja število spremenljivk
                    if len(line) == 1:
                        self.satisfied = 0  # robni primer imamo prazen OR -> not satisfied
                    clause.append(-1)
                    self.clauses.append(clause)

    # pregledamo, če se element ponavlja v vseh vrsticah
    def find_repeating(self):
        a = [set(x) for x in self.clauses]
        return set.intersection(*a)

    def dll_iterative(self):
        if self.satisfied == 0:
            return False, []

        repeating = self.find_repeating()
        if len(repeating) > 1:
            return True, ', '.join(str(x) for x in repeating)
        root_node = Node(None, None, None, 0)
        root_node.clauses = self.clauses
        tmp_node = root_node

        while True:
            if tmp_node.left == 0 and tmp_node.right == 0:
                l = tmp_node.literal
                if tmp_node.parent is None:
                    return False, []
                else:
                    tmp_node = tmp_node.parent
                    if l & 1 == 0:
                        tmp_node.left = 0
                    else:
                        tmp_node.right = 0
            elif tmp_node.left == 0:
                tmp_node = tmp_node.right
            else:
                status = is_sat(tmp_node.clauses)
                if status == 1:
                    return True, ' '.join(get_lit(x) for x in tmp_node.val)
                elif status == 0:
                    l = tmp_node.literal
                    if tmp_node.parent is None:
                        return False, []
                    else:
                        tmp_node = tmp_node.parent
                        if l & 1 == 0:
                            tmp_node.left = 0
                        else:
                            tmp_node.right = 0
                else:
                    l = get_branch_literal(tmp_node.clauses) | 1
                    left_node = Node(None, None, tmp_node, l ^ 1)
                    right_node = Node(None, None, tmp_node, l)
                    tmp_node.left = left_node
                    tmp_node.right = right_node
                    tmp_node = tmp_node.left


# razred vozliša, uporabljamo ga pri gradnji drevesa -> bolj prostorsko potrošno, manj potratno časovno,
# ko se moramo vračato nazaj, ker smo v trenutni veji dobili unsatisfiable, nam ni potrebno ponovno izračunati
# logične formule
class Node:
    def __init__(self, left, right, parent, literal):
        self.left = left
        self.right = right
        self.parent = parent
        self.literal = literal
        if parent is not None:
            self.val = copy.deepcopy(self.parent.val)
            self.clauses = simplify(copy.deepcopy(self.parent.clauses), literal)
            self.val.append(literal)
        else:
            self.val = []
            self.clauses = []

    def __str__(self):
        return "Literal: " + str(self.literal) + ", Clauses: " + str(self.clauses) + ", Val: " + str(self.val)


# lahko testiramo datoteke v direktoriju test_files
# UF - satisfiable
# UFF - unsatisfiable
# primer vhodnih parametrov - "run test UFF 1"
# to izvede testiranje na unsatisfiable primerih v podmapi 1
if sys.argv[1] == "run" and sys.argv[2] == "test":
    all_satisfiable = True
    if sys.argv[3][0:3] == "UFF":
        all_satisfiable = False

    testFiles = "test_files/" + sys.argv[3] + "/" + sys.argv[4] + "/"
    if os.path.isdir(testFiles):
        for filename in os.listdir(testFiles):
            t = time.time()
            s = SAT()
            s.read_file(testFiles + filename)
            if s.satisfied == 0:
                satisfied = False
            else:
                satisfied, val = s.dll_iterative()
            elapsed = time.time() - t
            if satisfied == all_satisfiable:
                print(filename + ": OK - TIME: " + str(elapsed)+" s")
            else:
                print("Wrong result in file: " + filename)
                break
    else:
        print(
            "Wrong use of 'run test' command! To use test command write command like 'python SAT_solver.py run test UFF 1' ")
# testiranje sudoku
elif sys.argv[1] == "sudoku":
    testFiles = ["sudoku_easy.txt", "sudoku_hard.txt", "sudoku_mini.txt"]
    testSolution = ["sudoku_easy_solution.txt", "sudoku_hard_solution.txt", "sudoku_mini_solution.txt"]
    for i in range(len(testFiles)):
        t = time.time()
        s = SAT()
        s.read_file("sudoku/" + testFiles[i])
        if s.satisfied == 0:
            satisfied = False
            val = '0'
        else:
            satisfied, val = s.dll_iterative()
        elapsed = time.time() - t

        with open("sudoku/"+testSolution[i], 'r') as f:
            firstLine = f.readline()
        solution = firstLine.split()
        solution = [int(x) for x in solution]
        solution = sorted(solution)

        our_solution = val.split()
        our_solution = [int(x) for x in our_solution]
        our_solution = sorted(our_solution)

        if our_solution == solution:
            print(testFiles[i]+": OK - TIME: "+str(elapsed)+" s")
        else:
            print(testFiles[i] + ": WRONG - TIME: " + str(elapsed)+" s")

# drugače sprejmemo dva vhodna parametra vhodno in izhodno datoteko
else:
    t = time.time()
    s = SAT()
    s.read_file(sys.argv[1])
    if s.satisfied == 0:
        satisfied = False
    else:
        satisfied, val = s.dll_iterative()
    text_file = open(sys.argv[2], "w")
    if satisfied:
        text_file.write(val)
    else:
        text_file.write("0")
    text_file.close()
    elapsed = time.time() - t
    print("TIME: " + str(elapsed)+" s")
