
def make_noduri():
    rez=[]
    for arc in arce:
        if int(arc[0]) not in rez:
            rez.append(int(arc[0]))
        if int(arc[2]) not in rez:
            rez.append(int(arc[2]))
    return rez

def make_delta():
    rez=[[] for _ in range(M+1)]
    rez[-1] = noduri #coloana de indici pentru denumirea fiecarui nod
    for y in range(M):
        for x in noduri:
            to_add=[]
            for arc in arce:
                if int(arc[0])==x and arc[1]==alfabet[y]:
                    to_add.append(int(arc[2]))
            rez[y].append(to_add)
    return rez

def find_index(x,lista):
    index = 0
    while str(lista[index])!=str(x):
        index+=1
    return index

def make_stare_noua(stari):
    delta[-1].append(stari)
    for col in range(M):
        temp = []
        for stare in stari:
            linie = find_index(int(stare), delta[-1])
            for x in delta[col][linie]:
                if x not in temp:
                    temp.append(x)
        delta[col].append(temp)


def make_delta_star():
    leg=[] #legaturile intre toate nodurile din delta_star
    coada = [q0] #coada lucreaza cu string-uri pt a putea avea si noduri cu nume de gen 01234
    adaug_in_coada = True
    while adaug_in_coada:
        adaug_in_coada = False
        nod = coada[-1]
        linie = find_index(nod,delta[-1])
        to_add=[]
        #cand creez o stare noua o adaug in delta dar in rest retin functia delta_star prin fiecare legatura din lista leg
        #urmand sa creez delta_star din aceasta lista
        for x in range(M):
            if len(delta[x][linie])<=1 and delta[x][linie]:
                leg.append(str(nod)+alfabet[x]+str(delta[x][linie][0]))
                #print("la nodul {} am adaugat legatura {}".format(nod,str(nod)+alfabet[x]+str(delta[x][linie][0])))
                if str(delta[x][linie][0]) not in coada:
                    if str(delta[x][linie][0]) not in to_add:
                        to_add.append(str(delta[x][linie][0]))
            elif len(delta[x][linie])>1:
                temp = ""
                for stare in delta[x][linie]:
                    temp += str(stare)
                leg.append(str(nod)+alfabet[x]+temp)
                #print("la nodul {} am adaugat legatura {}".format(nod,str(nod)+alfabet[x]+temp))
                if temp not in coada:
                    if temp not in to_add:
                        to_add.append(temp)
                make_stare_noua(temp)
        if to_add:
            coada.extend(to_add)
            adaug_in_coada=True
    coada.sort(key = lambda a: len(a))
    rez = [[] for _ in range(M + 1)]
    rez[-1] = coada
    for y in range(M):
        for x in rez[-1]:
            to_add = []
            for arc in leg:
                temp = 0
                while arc[temp] not in alfabet:
                    temp+=1
                if arc[0:temp] == x and arc[temp]==alfabet[y]:
                    to_add.append(arc[temp+1:])
            rez[y].append(to_add)
    return rez

def make_new_F():
    rez = []
    for x in delta_star[-1]:
        este_finala = False
        for stare in x:
            if stare in F:
                este_finala = True
        if este_finala:
            rez.append(x)
    return rez

def redenumeste(nume_stari):
    global N, q0, new_F
    new_N = len(delta_star[-1])
    N = new_N
    for x in range(len(delta_star[-1])):
        if delta_star[-1][x] != str(nume_stari[x]):
            to_replace = delta_star[-1][x]
            replacer = str(nume_stari[x])
            print("Inlocuiesc {} cu {}".format(to_replace,replacer))
            if to_replace == q0:
                q0 = replacer
            for y in range(len(new_F)):
                if new_F[y] == to_replace:
                    new_F[y] = replacer
            for y in range(M):
                for t in range(new_N):
                    if delta_star[y][t] and delta_star[y][t][0] == to_replace:
                        delta_star[y][t][0] = replacer
    delta_star[-1] = []
    for x in nume_stari:
        delta_star[-1].append(x)



#citire date de intrare nfa
f=open("input_for_nfa.txt")
inp = f.read().split()
f.close()
N = int(inp[0])    #numar stari
M = int(inp[1])    #numar litere
alfabet = [x for x in inp[2:M+2]]   #litere
q0 = inp[M+2]   #stare initiala
K = int(inp[M+3])   #numar stari finale
F = inp[M+4:M+4+K]  #starile finale
L = int(inp[M+4+K]) #numar legaturi intre stari
arce = [transf for transf in inp[M+5+K:]]   #legaturi intre stari

#construirea tabelului de valori pentru delta
noduri = sorted(make_noduri()) #am nevoie de noduri deoarece nu sunt neaparat numerotate de la 0 la N-1
delta = make_delta()

#eliminarea nedeterminismului
delta_star = make_delta_star()

#caclularea starilor finale noi
new_F = make_new_F()

#redenumirea starilor
redenumeste(range(len(delta_star[-1])))
#redenumeste([0,1,3,4]) #pt a returna la fel ca in exemplul din lab 3-4
print(delta_star)

#scrierea datelor de intrare pentru nfa-ul obtinut intr-un .txt pentru a putea fi prelucrat independent
new_arce=[]
for x in range(M):
    for y in range(N):
        for t in range(len(delta_star[x][y])):
            new_arce.append(str(delta_star[-1][y])+alfabet[x]+str(delta_star[x][y][t]))
arce = new_arce
L = len(arce)
F = new_F
K = len(F)

f=open("input_for_dfa.txt", "w") #mai intai deschid in mod write pt a si crea .txt-ul in caz ca nu exista
f.write("{}\n{}\n".format(N,M))
f.close()
f=open("input_for_dfa.txt", "a") #apoi il deschid in append ca sa nu suprascrie ce am adaugat deja si sa pot sa scriu mai usor
for letter in alfabet:
    f.write(letter+" ")
f.write("\n{}\n{}\n".format(q0,K))
for nod in F:
    f.write(str(nod)+" ")
f.write("\n{}\n".format(L))
for arc in arce:
    f.write(arc+"\n")
f.close()


