# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 18:41:36 2022

@author: seesc

processing text in df, preparing for modelling
"""
#regular imports
import pandas as pd

#nlp imports
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

'''
downloads = ['omw-1.4','genesis', 'wordnet', 'punkt', 'averaged_perceptron_tagger']

for d in downloads:
    nltk.download(d)
'''

#dataframe
df = pd.read_csv('qa_full.csv')


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
    #only keep acceptable chars
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

#remove na's so can go through knn()
df.fillna('', inplace = True)
#save to new df for ease of access later
df.to_csv('processed_qa.csv', index = False)
