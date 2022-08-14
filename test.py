# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 17:22:49 2022

@author: seesc

modelling using processed df
"""
from model2 import knn
import pandas as pd
from sklearn.model_selection import train_test_split


df = pd.read_csv('processed_qa.csv')
x = df[['question', 'snippet', 'description']]
y = df['truthValue']
xTrain, xTest, yTrain, yTest = train_test_split(x, y, random_state = 13)

mod = knn(k = 3, distanceType = 'path')
mod.fit(xTrain, yTrain)

print(mod.predict(xTest.iloc[0]))
print(yTest.iloc[0])
