# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 18:41:36 2022

@author: seesc

nlp for df
"""
#general
#import numpy as np
#from numpy import random
import pandas as pd
#import sklearn as skl
#import gensim #idk
#import matplotlib.pyplot as plt
#import re #idk
#from bs4 import BeautifulSoup

#from sklearn.metrics import roc_auc_score
#from sklearn.model_selection import train_test_split
#from sklearn.feature_extraction.text import CountVectorizer, TfidVectorizer
#from sklearn.metrics import accuracy_score, confusion_matrix



#nlp
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import genesis
from nltk.stem import WordNetLemmatizer
downloads = ['omw-1.4','genesis', 'wordnet', 'punkt', 'averaged_perceptron_tagger']
'''
for d in downloads:
    nltk.download(d)
'''
genesis_ic = wn.ic(genesis, False, 0.0)

from nltk.tokenize import word_tokenize
#from nltk.stem.porter import PorterStemmer
#from nltk.stem import SnowballStemmer
#from nltk.stem.lancaster import LancasterStemmer
#from nltk.corpus import stopwords as sw

#dataframe
df = pd.read_csv('qa_full.csv')

'''
class KNN_Classifier():
    def __init__(self, k = 3, distance_type = 'path'):
        self.k = k
        self.distance_type = distance_type

'''

#text processing with nltk
def clean(txt):
    txt = str(txt)

    #acceptable symbols, replace all others
    symbols = '1234567890!qwertyuiopasdfghjklzxcvbnm.\'\"-=+*/ '
    #dont want to remove negative stopwords (not, no, etc) so i made my own list
    #based off of stopwords.words('english')
    stopwords = ['a', 'am', 'an', 'and', 'are', 'as', 'at', 'be', 'but',
                'by', 'he', 'her', 'herself', 'him', 'himself', 'his', 'i', 'if',
                'in', 'into', 'me' 'my', 'myself', 'of', 'or', 'our', 'ours', 'ourselves',
                'she', 'so', 'the', 'their', 'theirs', 'them', 'themselves', 'then',
                'there', 'they', 'this', 'those', 'to', 'too', 'when', 'who', 'how', 'why',
                 'you', 'your', 'yours', '\'ve', '\'nt', '\'t']

    txt = txt.lower()
    #only get acceptable chars
    txt = ''.join(l for l in txt if l in symbols)
    #lemmatizing
    words = word_tokenize(txt)
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    #only get acceptable strings
    txt = ' '.join(w for w in words if w not in stopwords)

    return txt

cols = ['question', 'snippet', 'description']
for c in cols:
    df[c] = df[c].apply(clean)

df.to_csv('processed_qa.csv', index = False)
