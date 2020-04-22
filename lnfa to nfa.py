def lamda_closure(noduri):
    se_modifica=True
    while se_modifica:
        noduri_add = []
        se_modifica=False
        for nod_de_proc in noduri:
            for arc in arce:
                if arc[1]=="$" and int(arc[0])==nod_de_proc  and (int(arc[2]) not in noduri and int(arc[2]) not in noduri_add):
                    noduri_add.append(int(arc[2]))
                    se_modifica=True
        noduri.extend(noduri_add)
    return sorted(noduri)

def proceseaza_litera(noduri,litera):
    rez=[]
    for nod_de_proc in noduri:
        noduri_add = []
        for arc in arce:
            if int(arc[0])==nod_de_proc and arc[1]==litera and int(arc[2]) not in noduri_add and int(arc[2]) not in rez:
                noduri_add.append(int(arc[2]))
        rez.extend(noduri_add)
    return rez

def make_delta_star():
    rez=[[] for _ in range(M+1)]
    rez[-1]=[x for x in range(N)] #ultima coloana de indici pt a putea elimina mai usor duplicatele
    for y in range(M):
        for x in range(N):
            rez[y].append(lamda_closure(proceseaza_litera(lamda_closure([x]), alfabet[y])))
    return rez

def make_new_F():
    global K
    rez=[]
    for x in range(N):
        este_finala = False
        for nod in lamda_closure([x]):
            if str(nod) in F:
                este_finala = True
        if este_finala:
            rez.append(x)
    K = len(rez)
    return rez

def sunt_linii_identice_cu(y):
    rez=[y]
    actual_index = 0 #indexul adevarat al liniei care trebuie considerata
    while delta_star[-1][actual_index] != y:
        actual_index+=1
    for x in range(N):
        if x != actual_index:
            rez.append(x)
            for t in range(M):
                if delta_star[t][x] != delta_star[t][actual_index]:
                    rez.remove(x)
                    break
    return rez

def unite(linii):
    global N
    stare_noua = linii[0]
    #refacerea legaturilor intre noduri ca si cand as fi scos deja nodurile duplicate
    for y in range(M):
        for x in range(N):
            for t in range(len(delta_star[y][x])):
                if delta_star[y][x][t] in linii[1:]:
                    delta_star[y][x][t] = stare_noua

    #eliminarea legaturilor multiple rezultate
    for y in range(M):
        for x in range(N):
            delta_star[y][x] = list(set(delta_star[y][x]))

    #stergere linii propriu-zise
    x = 0
    while x < N:
        if delta_star[-1][x] in linii[1:]:
            print("Am eliminat linia starii {}".format(delta_star[-1][x]))
            for y in range(M+1):
                delta_star[y].pop(x)
            N-=1
        else:
            x+=1

#citire date de intrare lnfa
f=open("input_for_lnfa.txt")
inp = f.read().split()
f.close()
N = int(inp[0])    #numar stari
M = int(inp[1])    #numar litere
alfabet = [x for x in inp[2:M+2]]   #litere
alfabet.append("$") #adaug miscarea lamda
q0 = inp[M+2]   #stare initiala
K = int(inp[M+3])   #numar stari finale
F = inp[M+4:M+4+K]  #starile finale
L = int(inp[M+4+K]) #numar legaturi intre stari
arce = [transf for transf in inp[M+5+K:]]   #legaturi intre stari

#calculul functiei de tranzitie delta_star
delta_star = make_delta_star()
#calcularea starilor finale si initiale
new_F=make_new_F()

#Eliminarea starilor redundante
am_eliminari=True
while am_eliminari:
    am_eliminari=False
    x=0
    while x<N:
        am_eliminat_ceva=False
        linii = sunt_linii_identice_cu(delta_star[-1][x]) #primeste parametru indicele liniei nu linia si returneaza like-wise
        print("la starea {} am gasit liniile identice {}".format(delta_star[-1][x],linii))
        linii_din_F = [x for x in linii if x in new_F]
        linii_nu_din_F = [x for x in linii if x not in new_F]
        if len(linii_din_F) > 1:
            am_eliminat_ceva=True
            unite(linii_din_F)
        if len(linii_nu_din_F) > 1:
            am_eliminat_ceva=True
            unite(linii_nu_din_F)
        if am_eliminat_ceva:
            am_eliminari=True
            break
        x+=1

print(delta_star)
#update datele despre lnfa care au mai ramas
F = new_F
new_L = 0
for x in range(M):
    for y in range(N):
        new_L+=len(delta_star[x][y])
L = new_L
new_arce=[]
for x in range(M):
    for y in range(N):
        for t in range(len(delta_star[x][y])):
            new_arce.append(str(delta_star[-1][y])+alfabet[x]+str(delta_star[x][y][t]))
arce=new_arce
alfabet.remove("$")

#scrierea datelor de intrare pentru nfa-ul obtinut intr-un .txt pentru a putea fi prelucrat independent
f=open("input_for_nfa.txt", "w") #mai intai deschid in mod write pt a si crea .txt-ul in caz ca nu exista
f.write("{}\n{}\n".format(N,M))
f.close()
f=open("input_for_nfa.txt", "a") #apoi il deschid in append ca sa nu suprascrie ce am adaugat deja si sa pot sa scriu mai usor
for letter in alfabet:
    f.write(letter+" ")
f.write("\n{}\n{}\n".format(q0,K))
for nod in F:
    f.write(str(nod)+" ")
f.write("\n{}\n".format(L))
for arc in arce:
    f.write(arc+"\n")
f.close()