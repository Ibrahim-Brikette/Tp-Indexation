#Exercice1
def dictionary(filename):
    dictionary = {}
    with open (filename,"r",encoding="utf-8") as file :
        next(file)
        for line in file:
            key, value = line.strip().split("\t", 1)
            dictionary[key] = value
    return dictionary

#Exercice2
def recherche_naive(terme, documents):
    resultats = []
    for doc_id, texte in documents.items():
        if terme.lower() in texte.lower():
            resultats.append(doc_id)
    return resultats
documents = dictionary("documents.tsv")

#Exercice3
import re
def tokeniser(texte):
    return re.findall(r"\b\w+\b", texte.lower())

stopwords = {
 "le", "la", "les", "un", "une",
 "de", "des", "du", "et", "dans",
 "par", "pour", "d", "l"
}
def supprimer_stopwords(tokens):
    return [token for token in tokens if token not in stopwords]
tokens = tokeniser("L'indexation facilite l'accès rapide aux informations")
print (tokens)
print (supprimer_stopwords(tokens))

#Exercice4
def preprocess(text):
    tokens = tokeniser(text)
    return supprimer_stopwords(tokens)

def tokenize_corpus(documents):
    for d in documents.values():
        print(preprocess(d))
tokenize_corpus(documents)


#Exercice5
def construire_index(documents):
    index_inverse = {}
    for doc_id, texte in documents.items():
        termes = preprocess(texte)
        for terme in set(termes):
            if terme not in index_inverse:
                index_inverse[terme] = []
            index_inverse[terme].append(doc_id)

    return index_inverse

def construire_sorted_index(documents):
    return dict(sorted(construire_index(documents).items()))

#Exercice6
def recherche(terme,index_inverse):
    return index_inverse.get(terme.lower(),[])

print(construire_sorted_index(documents))

# terme = input("Entrez un terme : ")
for terme in ["documents","recherche","artificielle","collection","rapide"]:
    print("recherche naive de terme ",terme)
    print(recherche_naive(terme, documents))
    print("recherche avec index inversé de terme ", terme)
    print(recherche(terme,construire_sorted_index(documents)))
# they return the same list

#Exercice7
# a posting list (ou liste de postings) est
# simplement la liste des documents dans lesquels un terme apparaît.
def intersection_v(list1,list2):
    i = len(list1)
    j = len(list2)
    l = 0
    target = []
    non_target = []
    if j>i :
        l = i
        target = list1
        non_target = list2
    else:
        l = j
        target = list2
        non_target = list1
    common = []
    for k in range (l):
        if target[k] in non_target:
            common.append(target[k])
    return common

def intersection(list1, list2):
    i = 0
    j = 0
    resultat = []
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            resultat.append(list1[i])
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1
    return resultat
# terme = input("Entrez un 1er terme : ").lower()
# terme2 = input("Entrez un 2eme terme : ").lower()
#
for terme1,terme2  in [("documents","recherche"),("artificielle","collection"),("rapide","indexation")]:
    list1 = recherche(terme1,construire_sorted_index(documents))
    list2 = recherche(terme2,construire_sorted_index(documents))
    print("intersection avec skips de requete : ", terme1 ," AND ",terme2,"   ",intersection_v(list1,list2))

#Exercice 8

import time
def calculate_time(doc):
    debut = time.perf_counter()
    documents_100 = dictionary(doc)
    construire_sorted_index(documents_100)
    fin = time.perf_counter()
    print("Temps de construction  de index inverse pour ", doc, " :", fin - debut)

calculate_time("documents_100.tsv")
calculate_time("documents_1000.tsv")
calculate_time("documents_10000.tsv")

#Exercice 9
import math
def construire_skips(postings):
    n = len(postings)
    if n < 2:
        return {}
    steps = int(math.sqrt(n))
    skips = {}
    i = 0
    while (i + steps<n):
        skips[i] =  i + steps
        i+= steps
    return skips

def intersection_avec_skips(list1, list2,skips1,skips2):
    i = 0
    j = 0
    resultat = []
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            resultat.append(list1[i])
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            if i in skips1 and list1[skips1[i]] <= list2[j]:
                i = skips1[i]
            else:
                i += 1
        else:
            if j in skips2 and list2[skips2[j]] <= list1[i]:
                j = skips2[j]
            else:
                j += 1
    return resultat

list1 = recherche("indexation", construire_sorted_index(dictionary("documents_10000.tsv")))
list2 = recherche("classement", construire_sorted_index(dictionary("documents_10000.tsv")))
skips1 = construire_skips(list1)
skips2 = construire_skips(list2)

debut = time.perf_counter()
intersection(list1,list2)
fin = time.perf_counter()
print("Temps d execution d intersection sans skips  :", fin - debut)


debut = time.perf_counter()
intersection_avec_skips(list1,list2,skips1,skips2)
fin = time.perf_counter()
print("Temps d execution d intersection avec skips  :", fin - debut)
