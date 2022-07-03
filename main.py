import fileinput
import wikipedia
import re
import codecs
import numpy as np
import pandas as pd
import nltk

nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))

def removeNonAlphbets(word):
    text = re.sub("[^a-zA-Z]", "", word)
    re.sub(' +', '', text)
    return text
def removeStopWords(arr):
    allwords = ""
    for i in arr:
        allwords += (i.strip() + " ")
    word_tokens = allwords.split(" ")
    return [w.strip() for w in word_tokens if not w.strip().lower() in stop_words]

def createDictionaryOfAllWords(aritcle):
    createDictionaryOfAllWords.dictionary = {}
    arr = aritcle.split(" ")
    for i in range(len(arr)):
        arr[i] = removeNonAlphbets(arr[i])
    unique_words = set(arr)
    for i in unique_words:
        if i not in createDictionaryOfAllWords.dictionary.keys():
            createDictionaryOfAllWords.dictionary[i] = 0
    return createDictionaryOfAllWords.dictionary



def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))




def frequency(article):
    dictionary = {}
    arr = article.strip().split(" ")
    for i in range(len(arr)):
        arr[i] = removeNonAlphbets(arr[i])
    arr = removeStopWords(arr)
    unique_words = set(arr)
    for i in unique_words:
        print("--")
        if i not in dictionary.keys():
            dictionary[i] = 1
    for i in unique_words:
        dictionary[i]=arr.count(i)
        print(dictionary[i])
    return dictionary


def get_clusters(data, k):
    centroids = data.sample(n=k)
    clusters = [[] for _ in centroids.index]
    if type(data) is pd.DataFrame:
        while True:
            old_centroids = centroids.copy()
            for i in data.index:
                distances = []
                for j in centroids.index:
                    distances.append(euclidean_distance(data.loc[i], centroids.loc[j]))
                clusters[distances.index(np.min(distances))].append([x for x in data.loc[i]])
            if old_centroids.equals(centroids):
                break
            for i in range(k):
                centroids[i] = np.mean(clusters[i], axis=0)
    else:
        while True:
            old_centroids = centroids.copy()
            for i in data.index:
                distances = []
                for j in centroids.index:
                    distances.append(euclidean_distance(data[i], centroids[j]))
                clusters[distances.index(np.min(distances))].append(data[i])
            if old_centroids.equals(centroids):
                break
            for i in range(k):
                centroids[i] = np.mean(clusters[i], axis=0)

    return centroids, clusters


# with codecs.open("D:/Wikipedia/wikipedia/enwiki-20220401-pages-articles-multistream.xml", 'r', encoding="utf-8",
#                  errors='ignore') as file:
#     i = 0
#     for x in range(4000):
#         art = []
#         for line in file:
#             art.append(line)
#             print("--")
#             if line.find('</page>') > 0:
#                 break
#         output = codecs.open("output{}.txt".format(i), 'w', encoding="ASCII", errors='ignore')
#         for itr in art:
#             output.write("%s\n" % itr)
#         i+=1

AllDict = {}
articleDictionaries = []
with open("D:/Wikipedia/wikipedia/enwiki-20220401-pages-articles-multistream-index.txt") as infile:
    count = 4
    articles = []
    for line in infile:
        arr = line.split(':')
        print("article{} : {}".format(count, arr[2]))
        article = wikipedia.page(arr[2]).content
        articles.append([arr[2], article])
        count -= 1
        if count <= 0:
            break
    for article in articles:
        print("-------------------------------------------\n")
        print("count = {}".format(count))
        articleDictionaries.append(frequency(article[1]))
        dictF = createDictionaryOfAllWords(article[1])
        for (i, j) in dictF.items():
            AllDict[i] = j

    for i in range(len(articleDictionaries)):
        for n, v in AllDict.items():
            if n not in articleDictionaries[i]:
                articleDictionaries[i][n] = 0
    for key, value in AllDict.items():
        print("{} : {}".format(key, value), end=" ")

with open("input.csv", 'w') as file:
    for i, v in AllDict.items():
        file.write(i + ",")
    for itr in range(len(articleDictionaries)):
        for i, v in AllDict.items():
            file.write("{},".format(articleDictionaries[itr][i]))
        file.write("\n")
