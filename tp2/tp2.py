stopwords = {
 "le", "la", "les", "un", "une",
 "de", "des", "du", "et", "dans",
 "par", "pour", "d", "l","avec"
}
def dictionnary(filename):
    dict = {}
    with open (filename,"r",encoding = "utf-8") as file :
        for line in file:
            key ,  value = line.strip().split("\t",1)
            key = int(key.replace("doc",""))
            dict[key] = [token for token in tokeniser(value) if token  not in stopwords]
        return dict


def ordered_index(doc):
    # Parcours de tous les documents
    # Si T est le nombre total de termes dans tous les documents :
    # complexité approximative : O(T)
    index = {}
    dictio = dictionnary(doc)
    for doc_id,terms in dictio.items():
        for terme in set(terms) :
            if terme not in index:
                index[terme] = []
            index[terme].append(doc_id)
    # Tri des termes de l'index
    # Si V est le nombre de termes distincts :
    # complexité du tri : O(V log V)
    return dict(sorted(index.items()))


import re
def tokeniser(texte):
    return re.findall(r"\b\w+\b", texte.lower())

def intersection(terme1,terme2):
    liste1 = doc.get(terme1)
    liste2 = doc.get(terme2)
    i=0
    j=0
    intersection = []
    # On parcourt les deux listes une seule fois. #
    # Si n = len(liste1) et m = len(liste2) #
    # Complexité temporelle : # O(n + m) # # Complexité spatiale :
    # O(k) # où k = nombre de documents présents dans l'intersection.
    while  i <len(liste1) and j <len(liste2):
        if liste1[i] == liste2[j]:
            intersection.append(liste1[i])
            i+=1
            j+=1
        elif liste1[i] > liste2[j]:
            j+=1
        else:
            i+=1
    return intersection

import math
def create_skips(list1):
    # Création des skip pointers.
    # Comme on avance de 'steps' positions à chaque fois,
    # le nombre de skips créés est environ sqrt(n).
    # Complexité temporelle : O(sqrt(n))
    # Complexité spatiale : O(sqrt(n))
    n = len(list1)

    steps = int(math.sqrt(n))
    i = 0
    skips = {}
    while i+steps < n:
        skips[i] = i+steps
        i+=steps
def intersection_skip(terme1,terme2):
    liste1 = doc.get(terme1)
    skips1 = create_skips(liste1)
    liste2 = doc.get(terme2)
    skips2 = create_skips(liste2)
    i=0
    j=0
    intersection = []
    while  i <len(liste1) and j <len(liste2):
        if liste1[i] == liste2[j]:
            intersection.append(liste1[i])
            i+=1
            j+=1
        elif liste1[i] > liste2[j]:
            if j in skips2 and liste2[skips2[j]] <= liste1[i]:
                j = skips2[j]
            else:
                j+=1
        else:
            if i in skips1 and liste1[skips1[i]] <= liste2[j]:
                i = skips1[i]
            else:
                i+=1
    return intersection

#main
doc = ordered_index("documents.tsv")
print(doc)

terme = input("Entrez un 1er terme : ").lower()
terme2 = input("Entrez un 2eme terme : ").lower()
print(intersection_skip(terme,terme2))

