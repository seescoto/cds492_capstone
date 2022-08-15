# -*- coding: utf-8 -*-
"""
Created on Sat Aug  13 20:46:11 2022

@author: seesc

visualizations
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from model import knn

#import results (.npy in order to predict with different k's, .txt for results on k = 5)
with open('array0.npy', 'rb') as f:
    a0 = np.load(f, allow_pickle = True)
with open('array1.npy', 'rb') as f:
    a1 = np.load(f, allow_pickle = True)
with open('array2.npy', 'rb') as f:
    a2 = np.load(f, allow_pickle = True)
with open('array3.npy', 'rb') as f:
    a3 = np.load(f, allow_pickle = True)
with open('array4.npy', 'rb') as f:
    a4 = np.load(f, allow_pickle = True)
with open('array5.npy', 'rb') as f:
    a5 = np.load(f, allow_pickle = True)
arrays = (a0, a1, a2, a3, a4, a5)

df0 = pd.read_csv('df0.csv')
df1 = pd.read_csv('df1.csv')
df2 = pd.read_csv('df2.csv')
df3 = pd.read_csv('df3.csv')
df4 = pd.read_csv('df4.csv')
df5 = pd.read_csv('df5.csv')
dfs = (df0, df1, df2, df3, df4, df5)


def getAccuracies(k, dfs, arrays):
    accs = []
    for i in range(len(dfs)):
        x = dfs[i][['question', 'snippet', 'description']]
        y = dfs[i]['truthValue']
        xTrain, xTest, yTrain, yTest = train_test_split(x, y, random_state = 13,
                                                        test_size = 0.2, train_size = 0.8)
        mod = knn(k = k, distanceType = 'path')
        mod.fit(xTrain, yTrain)
        mod.xTest = xTest
        mod.adjMatrix = arrays[i]
        yPred = mod.predict()

        accuracy = metrics.accuracy_score(list(yTest.values), yPred)
        accs.append(accuracy)

    return accs

neighbors = range(1, 21)
results = [] #item = [#neighbors, accuracy]
for k in neighbors:
    #get k and then accuracies of all 6 dfs
    results.append([k , getAccuracies(k, dfs, arrays)])

#for i in results:
    #print(round(np.mean(i[1]), 3))
accs = [[i[0], np.mean(i[1])] for i in results]
print(accs)

#accuracy of different k's (1 - 15 ?) (plot 6 different points for each k - boxplot)

ks = []
for i in results:
    for x in range(6):
        ks.append(i[0])
accs = []
for i in results:
    for x in i[1]:
        accs.append(x)

#scatter plot with line w/ means
plt.figure(0)
plt.scatter(ks, accs, s = 3, c = 'slateblue')
kSmall = [i[0] for i in results]
meanAccs = [np.mean(i[1]) for i in results]
plt.plot(kSmall, meanAccs, lw = 3, c = 'slateblue')
plt.hlines(xmin = 0, xmax = 21, y = 0.5, color = 'red', linestyles = '--',
            label = '50% accuracy')
plt.xticks()
plt.ylabel('Accuracy')
plt.xlabel('# of neighbors')
plt.title('Accuracy of KNN using 80x20 Adjacency Matrices')
plt.savefig('accuracies-line.png')


plt.figure(1)
bp = plt.boxplot([i[1] for i in results])
for m in bp['medians']:
    m.set(color = 'darkviolet', linewidth = 2)
#plt.xticks(rotation = 90, fontsize = 6)
plt.hlines(xmin = 0, xmax = 21, y = 0.5, color = 'red', linestyles = '--',
            label = '50% accuracy', linewidth = 1.5)
plt.ylabel('Accuracy')
plt.xlabel('# of neighbors')
plt.title('Accuracy of KNN using 80x20 Adjacency Matrices')
plt.savefig('accuracies-box.png')
#
