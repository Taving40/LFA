f=open("input_for_lnfa.txt")

def proceseaza_lamda(stari_curente):
    global arce
    am_lamda=1
    while am_lamda:
        am_lamda=0
        for stare_de_proc in stari_curente:
            for tran in arce:
                if tran[0]==stare_de_proc and tran[1]=="$" and tran[2] not in stari_curente:
                    stari_curente.extend(tran[2])
                    am_lamda=1
    return stari_curente


def proceseaza_litera(stari_curente,litera):
    global arce,alfabet
    if litera not in alfabet:
        return []
    else:
        new_stari=[]
        for stare_de_proc in stari_curente:
            am_stari = []
            for tran in arce:
                if tran[0]==stare_de_proc and tran[1]==litera:
                    am_stari.append(tran[2])
            new_stari.extend(am_stari)
    return new_stari



def evaluate(cuvant):
    stari_curente =[q0]
    stari_curente = proceseaza_lamda(stari_curente)
    for litera in cuvant:
        stari_curente=proceseaza_litera(stari_curente,litera)
        stari_curente=proceseaza_lamda(stari_curente)
        print("La litera {} am starile {}".format(litera, stari_curente))
        if not stari_curente:
            return False
    for stare in stari_curente:
        if stare in F:
            return True
    return False


inp = f.read().split()
n = int(inp[0])     #numar stari
m = int(inp[1])    #numar litere
alfabet = [x for x in inp[2:m+2]]   #litere
alfabet.append("$")
q0 = inp[m+2]   #stare initiala
k = int(inp[m+3])   #numar stari finale
F = inp[m+4:m+4+k]  #starile finale
l = int(inp[m+4+k]) #numar legaturi intre stari
arce = [tran for tran in inp[m+5+k:]]   #legaturi intre stari

print((evaluate("ab")))

