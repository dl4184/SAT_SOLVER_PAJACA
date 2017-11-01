import random
import os


#začnemo s komentarjem označenim s "c"
#opišemo problem (cnf) in navedemo številom spremenljivk in stavkov
#stavek zaključimo z 0
#ni posebnega znaka za konec datoteke
def rand_dimacs(numvar, numclo, name,n=None):

    with open(name,"w",) as dim:
        print("c File: " + name, file=dim)
        print("c Authors: Domen, Gregor", file=dim)
        print("p cnf "+ str(numvar)+" "+str(numclo),file=dim )
        for i in range(numclo):
            if n is None:
                n2=random.randint(1,numvar)
                stev = random.sample(range(1, numvar + 1), n2)
            else:
                stev=random.sample(range(1,numvar+1),n)
            vrst=[str(k*random.choice([-1,1])) for k in stev]
            print(" ".join(vrst)+ " 0", file=dim)


nvar=[10,50,100,200]
nclo=[30,50,100,200,400,500,1000]

for i in nvar:
    for j in nclo:
        if i>=j:
            pass
        elif j>2**(2*i/3):
            pass
        else:
            os.makedirs("n{}_c{}".format(i,j))
            for k in range(10):
                rand_dimacs(i,j,"n{}_c{}/test{}.txt".format(i,j,k))
