import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer


# À faire une seule fois si nécessaire

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("punkt_tab")

STOPWORDS = set(stopwords.words("english"))

# Stemming
stemmer = PorterStemmer()
stemmer_fr = SnowballStemmer("french")

def original(doc):
    with open (doc,"r",encoding="utf-8") as f:

        for line in f:
            print(line)

stopwords = {
 "le", "la", "les", "un", "une",
 "de", "des", "du", "et", "dans",
 "par", "pour", "d", "l","avec","sans"
}
import re
def tokeniser(text):
    return re.findall(r"\b\w+\b", text.lower())
def process(text):
    text = text.lower()
    tokens = tokeniser(text)
    # tokens = [stemmer.stem(token) for token in tokens]
    return [token for token in tokens if token not in STOPWORDS]
def process_with_stemming(text):
    text = text.lower()
    tokens = tokeniser(text)
    tokens = [stemmer.stem(token) for token in tokens]
    return [token for token in tokens if token not in STOPWORDS]
def before_after(text):
    print("initial document:   ")
    print(text)
    print("tokens list")
    print(tokeniser(text))
    print("after processing")
    print(process(text))
def change_to_dict(doc):
    with open (doc,"r",encoding="utf-8") as f:
        dictionnary = {}
        for line in f:
            key, value = line.strip().split("\t", 1)
            dictionnary[key]=process(value)

    return dictionnary
def change_to_stemmed_dict(doc):
    with open (doc,"r",encoding="utf-8") as f:
        dictionnary = {}
        for line in f:
            key, value = line.strip().split("\t", 1)
            dictionnary[key]=process_with_stemming(value)

    return dictionnary

def construire_index_enrechi(dictionary):
    index_inverse = {}
    for doc_id, text in dictionary.items():
        terms = text
        for term in set(terms):
            tf = terms.count(term)
            if term not in index_inverse:
                index_inverse[term] = {
                    "df": 0,
                    "posting" : {}
                }
            index_inverse[term]["posting"][doc_id] = {
                "tf": tf,
            }
            index_inverse[term]["df"] +=1

    return index_inverse

def construire_sorted_index(dictionary):
    return dict(sorted(construire_index_enrechi(dictionary).items()))

import math
def calculer_idf(term, index_inverse, N):
    index = index_inverse.get(term)
    if index is None:
        return 0, 0
    else:
        df = index["df"]
        idf = math.log10(N / df)
        return df,idf

#main
dictionary = change_to_dict("documents.tsv")
dictionary_stemmed = change_to_stemmed_dict("documents.tsv")
index_inverse = construire_sorted_index(dictionary)
stemmed_index_inverse = construire_sorted_index(dictionary_stemmed)
print("le dictionnaire est :",dictionary)
print("l index inverse est :",construire_index_enrechi(dictionary))
vocabulary = sorted(index_inverse.keys())
print("le vocabulaire est: ",vocabulary)
print("information: ",index_inverse.get("information"))


terms = ["information","retrieval","vector","boolean"]

for term in terms:
    term = stemmer_fr.stem(term)

    df,idf  = calculer_idf(term,index_inverse,20)
    if df == 0 and idf == 0:
        print("terme ",term," doesn t have an index")

    else :
        print("the calculation results for the term '", term, "' are : ")
        print("df=  ", df)
        print("idf= ", idf)


def poids_tfidf(term, doc_id, index_inverse, N):
    index = index_inverse.get(term)
    if index is None:
        return 0,0
    posting = index.get("posting")

    if posting is None:
        return 0, 0
    doc = posting.get(doc_id)

    if doc is None:
        return 0, 0
    else :
        idf = calculer_idf(term, index_inverse, N)[1]
        tf = index.get("posting").get(doc_id).get("tf")
        if tf>0:
            w = (1+ math.log10(tf))*idf
        else :
            w =  0
        return tf,w

terms = ["embeddings","dense","retrieval","documents"]
for term in terms:
    # term = stemmer.stem(term)
    if (index_inverse.get(term) is None):
        print("term = ",term,"does not have an index")
    else:
        df,idf = calculer_idf(term,index_inverse,20)
        poids_tfidf(term,"D8",index_inverse,20)
        tf,w = poids_tfidf(term, "D8", index_inverse, 20)
        print("the calculation results for the term '", term, "' are : ")
        print("df=  ", df)
        print("idf= ", idf)
        print("tf= ", tf)
        print("w= ", w)


def document_vector(doc_id, vocabulary, index_inverse, N):

    vector = []
    nb_zero = 0
    for term in vocabulary:
        tf, weight = poids_tfidf(term, doc_id, index_inverse, N)

        vector.append(weight)

        if weight == 0:
            nb_zero += 1

    return vector,nb_zero

for doc in ["D1","D2","D3"]:
    vector,nb_zero = document_vector(doc, vocabulary, index_inverse, 20)
    print("document ",doc," vector is :"," with ",nb_zero,"  null components from a total of ",len(vector))
    print(vector)

def query_vector(query, vocabulary, index_inverse, N):
    terms = process(query)
    nb_zero = 0
    vector = []
    for term in vocabulary:
        tf = terms.count(term)
        if tf == 0:
            nb_zero += 1
            vector.append(0)
        else :
            index = index_inverse.get(term)
            if index is None:
                vector.append(0)
                nb_zero += 1
            else:
                df = index["df"]
                idf = math.log10(N / df)

                weight = (1 + math.log10(tf)) * idf

                vector.append(weight)
                print(term," : ",weight)
    return vector
def stemmed_query_vector(query, vocabulary, index_inverse, N):
    terms = process_with_stemming(query)
    nb_zero = 0
    vector = []
    for term in vocabulary:
        tf = terms.count(term)
        if tf == 0:
            nb_zero += 1
            vector.append(0)
        else :
            index = index_inverse.get(term)
            if index is None:
                vector.append(0)
                nb_zero += 1
            else:
                df = index["df"]
                idf = math.log10(N / df)

                weight = (1 + math.log10(tf)) * idf

                vector.append(weight)
                print(term," : ",weight)
    return vector
print("Query vector")
query = "Search engines use inverted indexes to retrieve documents efficiently so search engines are envolving"
query_vec = query_vector(query, vocabulary, index_inverse, 20)
print(query_vec)

import math

def cosine_similarity(vector1, vector2):

    dot_product = 0.0
    norm1 = 0.0
    norm2 = 0.0

    for i in range(len(vector1)):
        dot_product += vector1[i] * vector2[i]
        norm1 += vector1[i] ** 2
        norm2 += vector2[i] ** 2

    norm1 = math.sqrt(norm1)
    norm2 = math.sqrt(norm2)

    if norm1 == 0 or norm2 == 0:
        return 0

    return dot_product / (norm1 * norm2)
doc_vector,nb_zero = document_vector(doc, vocabulary, index_inverse, 20)
print("la simularite entre :")
print(query)
print(" et le document")
similarity = cosine_similarity(
    query_vec,
    doc_vector
)

print(similarity)

def search(query, documents, index_inverse, vocabulary, N, k=5):
    # preprocess(query)
    terms = process(query)
    # construire le vecteur requête
    vector_query = query_vector(query, vocabulary, index_inverse, N)
    # calculer sim(q, Di) pour chaque document
    similarities = {}
    for doc in documents:
        similarities[doc] = cosine_similarity(vector_query, document_vector(doc,vocabulary, index_inverse, N)[0])
    # éliminer les scores nuls
    not_null_dict = { k: v for k,v in similarities.items() if v != 0.0}
    # trier par score décroissant
    not_null_dict = dict(sorted(not_null_dict.items(), key=lambda item: item[1], reverse=True))
    # retourner les k premiers résultats
    return dict(list(not_null_dict.items())[:k])
def stemmed_search(query, documents, index_inverse, vocabulary, N, k=5):
    # preprocess(query)
    terms = process(query)
    # construire le vecteur requête
    vector_query = stemmed_query_vector(query, vocabulary, index_inverse, N)
    # calculer sim(q, Di) pour chaque document
    similarities = {}
    for doc in documents:
        similarities[doc] = cosine_similarity(vector_query, document_vector(doc,vocabulary, index_inverse, N)[0])
    # éliminer les scores nuls
    not_null_dict = { k: v for k,v in similarities.items() if v != 0.0}
    # trier par score décroissant
    not_null_dict = dict(sorted(not_null_dict.items(), key=lambda item: item[1], reverse=True))
    # retourner les k premiers résultats
    return dict(list(not_null_dict.items())[:k])

def boolean_and_search(query,index_inverse):

    terms = process(query)

    result = set(index_inverse.get(terms[0])["posting"].keys())
    for term in terms[1:]:
        if term not in index_inverse :
            return []
        documents = set(index_inverse.get(term)["posting"].keys())

        result = result & documents
    return sorted(result)

    similarities = {}
    for doc in documents:
        similarities[doc] = cosine_similarity(vector_query, document_vector(doc,vocabulary, index_inverse, N)[0])
    # éliminer les scores nuls
    not_null_dict = { k: v for k,v in similarities.items() if v != 0.0}
    # trier par score décroissant
    not_null_dict = dict(sorted(not_null_dict.items(), key=lambda item: item[1], reverse=True))
    # retourner les k premiers résultats
    return dict(list(not_null_dict.items())[:k])

k= int(input("donner le nombre k pour le ranking"))
search_query = "information retrieval model"
search_result = search(search_query,dictionary.keys(),index_inverse, vocabulary,20 )
print(search_result)
i= 0
print("TOP-5 RESULTS WITHOUT STEMMING ")
print()
print()
print("Rank   DocID     Score                       Document ")
for doc in search_result:
    i=i+1
    print(i,"      ",doc,"     ",search_result[doc],"       ",dictionary[doc])




search_query = "information retrieval model"
stemmed_vocabulary = sorted(stemmed_index_inverse.keys())
search_result = stemmed_search(search_query,dictionary_stemmed.keys(),stemmed_index_inverse, stemmed_vocabulary,20 )
print(search_result)
i= 0
print("TOP-5 RESULTS WITH STEMMING ")
print()
print("Rank   DocID     Score                       Document ")
for doc in search_result:
    i=i+1
    print(i,"      ",doc,"     ",search_result[doc],"       ",dictionary_stemmed[doc])



query = "information retrieval model"
print("boolean search results")
print(boolean_and_search(query, index_inverse))

print("----------TOP 5 AVEC DE 5 REQUETE------------")
queries = ["Search engines","Stop words are commonly removed with stemming","retrieved documents","Boolean retrieval learning","BM25 is a ranking function"]
for query in queries:
    search_result = search(query, dictionary.keys(), index_inverse, vocabulary, 20)
    print("query:",query)
    print("TOP-5 RESULTS")
    print()
    print()
    print("Rank   DocID     Score                       Document ")
    for doc in search_result:
        i = i + 1
        print(i, "      ", doc, "     ", search_result[doc], "       ", dictionary[doc])


