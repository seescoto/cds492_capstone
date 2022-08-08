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
#from nltk.corpus import wordnet as wn
#from nltk.stem import WordNetLemmatizer

#data uploading & splitting
df = pd.read_csv('processed_qa.csv')
x = df[['question', 'snippet', 'description']]
y = df['truthValue']
xTrain, xTest, yTrain, yTest = train_test_split(x, y, random_state = 13)

###training
mod = knn(k = 5, distanceType = 'path')
mod.fit(xTrain, yTrain)

yPred = mod.predict(xTest)

print("Accuracy: ", metrics.accuracy_score(yTest, yPred))
