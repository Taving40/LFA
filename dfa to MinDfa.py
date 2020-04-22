def make_delta():
    global N, M, stari
    rez = [[] * N for _ in range(M)]
    rez.append(stari)
    for y in range(M):
        for x in stari:
            to_add = []
            for arc in arce:
                if int(arc[0]) == x and arc[1] == alfabet[y]:
                    to_add.append(int(arc[2]))
            if to_add:
                rez[y].append(to_add[0])
            else:
                rez[y].append(to_add)
    return rez


def make_bool_delta():
    global N, M, stari, delta, alfabet
    rez = [[True] * N for _ in range(N)]
    rez.append(stari)
    for y in range(N):
        # print()
        for x in range(N):
            # print("Compar {} cu {}".format(rez[-1][x], rez[-1][y]))
            if (str(rez[-1][stari[x]]) in F and str(rez[-1][stari[y]]) not in F) or (
                    str(rez[-1][stari[x]]) not in F and str(rez[-1][stari[y]]) in F):
                rez[y][x] = False

    am_modificat = True
    while am_modificat:
        am_modificat = False
        for y in range(N):
            for x in range(N):
                for t in range(M):
                    # print("Verific daca rez[delta[t][y]][delta[t][x]]={} este fals.".format( rez[delta[t][y]][delta[t][x]]))
                    if delta[t][y] and delta[t][x] and (rez[delta[t][y]][delta[t][x]] == False):
                        rez[y][x] = False
    return rez


def sterge_linia_cu_x(x, array):
    poz = 0
    while array[-1][poz] != x:
        poz += 1
    for y in range(len(array)):
        del array[y][poz]
    return array


def get_line(x, array):
    rez = []
    for i in range(len(array)):
        rez.append(array[i][x])
    return rez


def make_delta_star():
    global bool_delta, delta, N, M, new_stari
    for y in range(N):
        stare_noua = [stari[y]]
        for x in range(N):
            if bool_delta[y][x] == True:
                if stari[x] not in stare_noua:
                    stare_noua.append(stari[x])
        if sorted(stare_noua) not in new_stari:
            new_stari.append(sorted(stare_noua))
    rez = [x for x in delta]
    for y in range(M + 1):
        for x in range(N):
            for t in range(len(new_stari)):
                if rez[y][x] in new_stari[t]:
                    rez[y][x] = new_stari[t]
    #print(rez)
    rez2 = [[] * len(rez[-1]) for _ in range(M + 1)]
    for y in range(len(rez[-1])):
        linief = get_line(y, rez)
        for x in range(len(rez[-1])):
            if y != x and rez[-1][y] == rez[-1][x]:
                linie = get_line(x, rez)
                for t in range(len(linief)):
                    if not linief[t] and linie[t]:
                        linief[t] = linie[t]
        if rez[-1][y] not in rez2[-1]:
            for t in range(len(rez2)):
                rez2[t].append(linief[t])
    return rez2

def make_dead_end():
    global delta_star, N, M, new_stari, new_F
    not_dead = [x for x in new_F]
    dead = []
    for _ in range(len(new_stari)):
        for y in range(len(delta_star)):
            for x in range(len(delta_star[-1])):
                if delta_star[-1][x] not in not_dead and delta_star[y][x] in not_dead:
                    not_dead.append(delta_star[-1][x])
    for x in range(len(delta_star[-1])):
        for y in range(len(delta_star)):
            if delta_star[y][x] not in not_dead and delta_star[y][x] not in dead:
                dead.append(delta_star[y][x])
    return dead


def make_ne_accesibil():
    global delta_star, N, M, new_stari
    accesibil = [q0]
    ne_accesibil = []
    for _ in range(len(new_stari)):
        for y in range(len(delta_star)):
            for x in range(len(delta_star[-1])):
                if delta_star[-1][x] in accesibil and delta_star[y][x] not in accesibil:
                    accesibil.append(delta_star[y][x])
    for x in range(len(delta_star[-1])):
        for y in range(len(delta_star)):
            if delta_star[y][x] not in accesibil and delta_star[y][x] not in ne_accesibil:
                ne_accesibil.append(delta_star[y][x])
    return ne_accesibil


def list_to_str(lista):
    rez = ""
    for x in lista:
        rez += str(x)
    return rez


# citire date de intrare dfa
f = open("input_for_dfa.txt")
inp = f.read().split()
f.close()
N = int(inp[0])  # numar stari
M = int(inp[1])  # numar litere
alfabet = [x for x in inp[2:M + 2]]  # litere
q0 = inp[M + 2]  # stare initiala
K = int(inp[M + 3])  # numar stari finale
F = inp[M + 4:M + 4 + K]  # starile finale
L = int(inp[M + 4 + K])  # numar legaturi intre stari
arce = [transf for transf in inp[M + 5 + K:]]  # legaturi intre stari

# construirea matricei de echivalenta (determinarea starilor de echivalenta)
stari = []  # am nevoie de multimea de stari deoarece nu stiu sigur ca starile sunt numerotate de la 0 la N
for x in arce:
    if int(x[0]) not in stari:
        stari.append(int(x[0]))
    if int(x[-1]) not in stari:
        stari.append(int(x[-1]))
stari = sorted(stari)

delta = make_delta()
print(delta)

bool_delta = make_bool_delta()
print(bool_delta)

# gruparea starilor echivalente si calcularea functiei de tranzitie delta_star
new_stari = []
delta_star = make_delta_star()
print(delta_star)

# calcularea starilor finale si initiale
for x in delta_star:
    for y in x:
        if int(q0) in y:
            new_q0 = y
            break
q0 = new_q0

new_F = []
for x in delta_star:
    for y in x:
        for z in y:
            if str(z) in F:
                if y not in new_F:
                    new_F.append(y)
F = new_F

# eliminarea starilor dead-end
dead_end = make_dead_end()
# print(dead_end)
if x in delta_star[-1]:
    for x in dead_end:
        sterge_linia_cu_x(x, delta_star)
for y in range(len(delta_star)):
    for x in range(len(delta_star[-1])):
        if delta_star[y][x] in dead_end:
            delta_star[y][x] = []

# eliminarea starilor neaccesibile
ne_accesibil = make_ne_accesibil()
# print(ne_accesibil)
for x in ne_accesibil:
    sterge_linia_cu_x(x, delta_star)
for y in range(len(delta_star)):
    for x in range(len(delta_star[-1])):
        if delta_star[y][x] in ne_accesibil:
            delta_star[y][x] = []

# afisare finala
N = len(delta_star[-1])
K = len(F)
new_arce = []
for x in range(M):
    for y in range(N):
        if delta_star[x][y]:
            new_arce.append(list_to_str(delta_star[-1][y]) + alfabet[x] + list_to_str(delta_star[x][y]))
arce = new_arce
L = len(arce)
q0 = list_to_str(q0)
for x in range(len(F)):
    F[x] = list_to_str(F[x])

f = open("final.txt", "w")
f.write("{}\n{}\n".format(N, M))
f.close()
f = open("final.txt", "a")
for letter in alfabet:
    f.write(letter + " ")
f.write("\n{}\n{}\n".format(q0, K))
for nod in F:
    f.write(str(nod) + " ")
f.write("\n{}\n".format(L))
for arc in arce:
    f.write(arc + "\n")
f.close()
