# -*- coding: utf-8 -*-
"""
Created on Thur Aug  11 23:07:54 2022

@author: seesc

test code for bug fixing (can delete when full model has been sorted out)
"""

from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from model import knn
from sklearn import metrics

with open('array0.npy', 'rb') as f:
    mat = np.load(f, allow_pickle = True)

df0 = pd.read_csv('df0.csv')
x = df0[['question', 'snippet', 'description']]
y = df0['truthValue']
xTrain, xTest, yTrain, yTest = train_test_split(x, y, random_state = 13,
                                                    test_size = 0.2, train_size = 0.8)

mod = knn(k = 5)
mod.fit(xTrain, yTrain)
mod.adjMatrix = mat
mod.xTest = xTest
yPred = mod.predict()

print(metrics.accuracy_score(list(yTest.values), yPred))
