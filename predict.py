# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 01:29:04 2022

@author: seesc

modelling
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
from model import knn
import matplotlib.pyplot as plt
import nltk
import statistics as stat
#from nltk.corpus import wordnet as wn
#from nltk.stem import WordNetLemmatizer

#data uploading & splitting
df = pd.read_csv('processed_qa.csv')

'''
x = df[['question', 'snippet', 'description']]
y = df['truthValue']
xTrain, xTest, yTrain, yTest = train_test_split(x, y, random_state = 13)
'''
#split into 6 dfs, because toSynsets takes so long each one will take ~1hr to create 80x20 adjMatrix
#rest of computation is pretty fast, so save the adjMatrix and do new predictions on that instead

parts = np.array_split(df.sample(frac = 1), 6)
matrices = [] #list of np arrays

for p in range(len(parts)):
    x = parts[p][['question', 'snippet', 'description']]
    y = parts[p]['truthValue']
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, random_state = 13,
                                                    test_size = 0.2, train_size = 0.8)
    mod = knn(k = 5, distanceType = 'path')
    mod.fit(xTrain, yTrain)
    mod.process(xTest) #creates adjacency matrix
    yPred = mod.predict()

    #save matrix as array_p_.npy where _p_ = loop number
    #just in case quits halfway thru, dont lose all progress
    file = 'array' + str(p) + '.npy'
    with open(file, 'wb') as f:
        np.save(f, mod.adjMatrix)
    matrices.append(mod.adjMatrix)

    #predictions, save predictions
    file = 'pred' + str(p) + '.txt'
    with open(file, 'w') as f:
        f.write('truthValue \t\t\t predicted truthValue')
        for y in range(len(yPred)):
            f.write("\n" + str(yTest[y] + "\t\t\t" + str(yPred[y])))

    print('part ' + str(p) + ' complete')
    print("Accuracy: ", metrics.accuracy_score(yTest, yPred))

#now save all matrices
with open('fullArray.npy', 'wb') as f:
    np.save(f, matrices)

'''
save np array to .npy file

with open('test.npy', 'wb') as f:
    np.save(f, np.array([1, 2]))
    np.save(f, np.array([1, 3]))


retrieve np array from .npy file

with open('test.npy', 'rb') as f:
    a = np.load(f)
    b = np.load(f)
'''
