f=open("input_for_lnfa.txt")

def proceseaza_litera(noduri_acum,litera):
    if litera not in alfabet:
        return []
    else:
        noduri_noi=[]
        for nod_de_proc in noduri_acum:
            am_noduri = []
            for arc in arce:
                if arc[0]==nod_de_proc and arc[1]==litera:
                    am_noduri.append(arc[2])
            noduri_noi.extend(am_noduri)
    return noduri_noi

def proceseaza_lamda(noduri_acum):
    se_modifica=True
    while se_modifica:
        se_modifica=False
        for nod_de_proc in noduri_acum:
            for arc in arce:
                if arc[1]=="$" and arc[0]==nod_de_proc  and arc[2] not in noduri_acum:
                    noduri_acum.append(arc[2])
                    se_modifica=True
    return noduri_acum

def evalueaza(cuvant):
    noduri_acum =[q0]
    noduri_acum = proceseaza_lamda(noduri_acum)
    for litera in cuvant:
        noduri_acum=proceseaza_litera(noduri_acum,litera)
        noduri_acum=proceseaza_lamda(noduri_acum)
        print("La litera {} am starile {}".format(litera, noduri_acum))
    for nod in noduri_acum:
        if nod in F:
            return True
    return False


inp = f.read().split()
N = int(inp[0])    #numar stari
M = int(inp[1])    #numar litere
alfabet = [x for x in inp[2:M+2]]   #litere
alfabet.append("$") #adaug miscarea lamda
q0 = inp[M+2]   #stare initiala
K = int(inp[M+3])   #numar stari finale
F = inp[M+4:M+4+K]  #starile finale
L = int(inp[M+4+K]) #numar legaturi intre stari
arce = [transf for transf in inp[M+5+K:]]   #legaturi intre stari

cuvant = input("Introduceti ce cuvant doriti sa evaluati: ")
bool = evalueaza(cuvant)
if bool==True:
    print("Cuvantul ales este acceptat.")
else:
    print("Cuvantul ales nu este acceptat")


