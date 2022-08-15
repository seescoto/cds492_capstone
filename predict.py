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

#data uploading & splitting
df = pd.read_csv('processed_qa.csv')

'''
x = df[['question', 'snippet', 'description']]
y = df['truthValue']
xTrain, xTest, yTrain, yTest = train_test_split(x, y, random_state = 13)
'''
#split into 6 dfs, because toSynsets takes so long each one will take ~1hr to create 80x20 adjMatrix
#rest of computation is pretty fast, so save the adjMatrix and do more predictions (different k's)

parts = np.array_split(df.sample(frac = 1), 6)
matrices = [] #list of np arrays

for p in range(len(parts)):
    #save into new df
    file = 'df' + str(p) + '.csv'
    parts[p].to_csv(file, index = False)


    x = parts[p][['question', 'snippet', 'description']]
    y = parts[p]['truthValue']
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, random_state = 13,
                                                    test_size = 0.2, train_size = 0.8)
    mod = knn(k = 5, distanceType = 'path')
    mod.fit(xTrain, yTrain)
    mod.process(xTest) #creates adjacency matrix

    #save matrix as arrayP.npy where P = loop number
    #just in case quits halfway through, we dont lose all progress
    file = 'array' + str(p) + '.npy'
    with open(file, 'wb') as f:
        np.save(f, mod.adjMatrix)
    matrices.append(mod.adjMatrix)

    #get and save predictions
    yPred = mod.predict()

    #save predictions as predP.txt where P = loop number
    file = 'pred' + str(p) + '.txt'
    with open(file, 'w') as f:
        f.write('truthValue \t\t\t predicted truthValue')
        for y in range(len(yPred)):
            f.write("\n" + str(list(yTest)[y]) + "\t\t\t" + str(yPred[y]))

    print('part ' + str(p) + ' complete')
    print("Accuracy: ", metrics.accuracy_score(list(yTest.values), yPred))

#now save all matrices together
with open('fullArray.npy', 'wb') as f:
    np.save(f, matrices)
